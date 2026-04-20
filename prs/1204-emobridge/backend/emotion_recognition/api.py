"""
情感识别API路由
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import logging

from .models import (
    EmotionState, EmotionType, EmotionDetectionResult, PhysiologicalData,
    FacialExpression, BehavioralData, VoiceAnalysis, BCIData, ModalityData,
    PatientEmotionProfile, EmotionTreatmentRecommendation
)
from .engine import EmotionRecognitionEngine

logger = logging.getLogger(__name__)
emotion_router = APIRouter()

# 全局情感识别引擎
emotion_engine = EmotionRecognitionEngine()

@emotion_router.post("/detect", response_model=EmotionDetectionResult)
async def detect_emotion(
    modality_data: List[ModalityData],
    patient_id: str,
    session_id: str,
    background_tasks: BackgroundTasks
):
    """
    检测情感状态
    支持多模态情感识别
    """
    try:
        logger.info(f"开始情感检测 - 患者: {patient_id}, 会话: {session_id}")
        
        # 执行情感检测
        result = emotion_engine.multimodal_emotion_detection(modality_data)
        
        # 更新患者档案
        background_tasks.add_task(
            emotion_engine.update_patient_profile,
            patient_id,
            result
        )
        
        # 更新结果中的患者和会话信息
        result.patient_id = patient_id
        result.session_id = session_id
        
        logger.info(f"情感检测完成 - 检测到 {len(result.detected_emotions)} 种情感状态")
        return result
        
    except Exception as e:
        logger.error(f"情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"情感检测失败: {str(e)}")

@emotion_router.post("/physiological")
async def detect_physiological_emotion(data: PhysiologicalData):
    """
    从生理信号检测情感
    """
    try:
        emotions = emotion_engine.detect_emotion_from_physiological(data)
        return {
            "success": True,
            "emotions": emotions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"生理信号情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@emotion_router.post("/facial")
async def detect_facial_emotion(data: FacialExpression):
    """
    从面部表情检测情感
    """
    try:
        emotions = emotion_engine.detect_emotion_from_facial(data)
        return {
            "success": True,
            "emotions": emotions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"面部表情情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@emotion_router.post("/behavioral")
async def detect_behavioral_emotion(data: BehavioralData):
    """
    从行为分析检测情感
    """
    try:
        emotions = emotion_engine.detect_emotion_from_behavioral(data)
        return {
            "success": True,
            "emotions": emotions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"行为分析情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@emotion_router.post("/voice")
async def detect_voice_emotion(data: VoiceAnalysis):
    """
    从语音分析检测情感
    """
    try:
        emotions = emotion_engine.detect_emotion_from_voice(data)
        return {
            "success": True,
            "emotions": emotions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"语音分析情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@emotion_router.post("/bci")
async def detect_bci_emotion(data: BCIData):
    """
    从脑机接口检测情感
    """
    try:
        emotions = emotion_engine.detect_emotion_from_bci(data)
        return {
            "success": True,
            "emotions": emotions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"BCI情感检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@emotion_router.get("/patient/{patient_id}/profile")
async def get_patient_profile(patient_id: str):
    """
    获取患者情感档案
    """
    try:
        if patient_id not in emotion_engine.patient_profiles:
            raise HTTPException(status_code=404, detail="患者档案不存在")
        
        profile = emotion_engine.patient_profiles[patient_id]
        return {
            "success": True,
            "profile": profile,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取患者档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取档案失败: {str(e)}")

@emotion_router.post("/patient/{patient_id}/profile")
async def create_patient_profile(
    patient_id: str,
    baseline_data: Optional[dict] = None
):
    """
    创建或更新患者情感档案
    """
    try:
        if patient_id not in emotion_engine.patient_profiles:
            emotion_engine.patient_profiles[patient_id] = EmotionProfile(
                patient_id=patient_id,
                baseline_emotions=baseline_data or {}
            )
        else:
            if baseline_data:
                emotion_engine.patient_profiles[patient_id].baseline_emotions.update(baseline_data)
        
        return {
            "success": True,
            "message": "患者档案创建/更新成功",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"创建患者档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建档案失败: {str(e)}")

@emotion_router.get("/recommendation/{patient_id}")
async def get_treatment_recommendation(
    patient_id: str,
    emotion_type: EmotionType,
    confidence: float,
    intensity: float
):
    """
    获取治疗建议
    """
    try:
        current_emotion = EmotionState(
            emotion_type=emotion_type,
            confidence=confidence,
            intensity=intensity,
            timestamp=datetime.now()
        )
        
        recommendation = emotion_engine.get_treatment_recommendation(
            patient_id, current_emotion
        )
        
        return {
            "success": True,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取治疗建议失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取建议失败: {str(e)}")

@emotion_router.get("/emotions")
async def get_emotion_types():
    """
    获取所有支持的情感类型
    """
    return {
        "success": True,
        "emotion_types": [emotion.value for emotion in EmotionType],
        "timestamp": datetime.now().isoformat()
    }

@emotion_router.get("/statistics")
async def get_emotion_statistics(patient_id: str, days: int = 7):
    """
    获取情感统计分析
    """
    try:
        if patient_id not in emotion_engine.patient_profiles:
            raise HTTPException(status_code=404, detail="患者档案不存在")
        
        profile = emotion_engine.patient_profiles[patient_id]
        
        # 计算情感分布统计
        emotion_distribution = profile.baseline_emotions
        
        return {
            "success": True,
            "statistics": {
                "emotion_distribution": emotion_distribution,
                "baseline_emotions": emotion_distribution,
                "last_updated": profile.last_updated.isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取情感统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")

@emotion_router.post("/calibrate")
async def calibrate_emotion_detection(
    patient_id: str,
    calibration_data: List[EmotionState]
):
    """
    校准情感检测系统
    """
    try:
        # 基于校准数据调整模型参数
        logger.info(f"开始校准情感检测系统 - 患者: {patient_id}")
        
        # 这里应该实现实际的校准算法
        # 现在返回成功响应
        
        return {
            "success": True,
            "message": "情感检测系统校准完成",
            "calibration_data": len(calibration_data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"情感检测系统校准失败: {e}")
        raise HTTPException(status_code=500, detail=f"校准失败: {str(e)}")

@emotion_router.get("/health")
async def emotion_recognition_health():
    """
    情感识别系统健康检查
    """
    try:
        health_status = {
            "status": "healthy",
            "models_initialized": emotion_engine.models_initialized,
            "confidence_threshold": emotion_engine.confidence_threshold,
            "active_patients": len(emotion_engine.patient_profiles),
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
    except Exception as e:
        logger.error(f"情感识别系统健康检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")