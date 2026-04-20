"""
数字孪生API路由
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from .models import (
    PatientDigitalTwin, TwinState, TwinStateType, TwinUpdateRequest,
    PredictionResult, PredictionType, TreatmentSimulation, CrisisDetectionResult,
    TwinQueryRequest
)
from .engine import DigitalTwinEngine

from ..emotion_recognition.models import EmotionState

logger = logging.getLogger(__name__)
twin_router = APIRouter()

# 全局数字孪生引擎
twin_engine = DigitalTwinEngine()

@twin_router.post("/create/{patient_id}")
async def create_patient_twin(patient_id: str):
    """
    创建患者数字孪生
    """
    try:
        twin = twin_engine.create_patient_twin(patient_id)
        return {
            "success": True,
            "message": f"患者 {patient_id} 的数字孪生创建成功",
            "twin": twin.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建数字孪生失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@twin_router.post("/update")
async def update_twin_state(update_request: TwinUpdateRequest):
    """
    更新数字孪生状态
    """
    try:
        twin = twin_engine.update_twin_state(update_request)
        return {
            "success": True,
            "message": "数字孪生状态更新成功",
            "twin": twin.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新数字孪生状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

@twin_router.get("/{patient_id}/state")
async def get_current_twin_state(patient_id: str):
    """
    获取当前数字孪生状态
    """
    try:
        if patient_id not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail="患者数字孪生不存在")
        
        twin = twin_engine.patient_twins[patient_id]
        return {
            "success": True,
            "current_state": twin.current_state.dict(),
            "last_updated": twin.updated_at.isoformat(),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取数字孪生状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取状态失败: {str(e)}")

@twin_router.get("/{patient_id}/history")
async def get_twin_state_history(patient_id: str, limit: int = 100):
    """
    获取数字孪生历史状态
    """
    try:
        if patient_id not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail="患者数字孪生不存在")
        
        history = twin_engine.get_twin_state_history(patient_id, limit)
        return {
            "success": True,
            "history": [state.dict() for state in history],
            "total_records": len(history),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取历史状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取历史失败: {str(e)}")

@twin_router.post("/predict/emotion-transition/{patient_id}")
async def predict_emotion_transition(
    patient_id: str,
    hours_ahead: float = 24
):
    """
    预测情感转换
    """
    try:
        prediction = twin_engine.predict_emotion_transition(patient_id, hours_ahead)
        return {
            "success": True,
            "prediction": prediction.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"情感转换预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")

@twin_router.post("/predict/treatment-response/{patient_id}")
async def predict_treatment_response(
    patient_id: str,
    treatment_plan: Dict[str, Any]
):
    """
    预测治疗响应
    """
    try:
        prediction = twin_engine.predict_treatment_response(patient_id, treatment_plan)
        return {
            "success": True,
            "prediction": prediction.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"治疗响应预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")

@twin_router.get("/crisis-detection/{patient_id}")
async def detect_crisis(patient_id: str):
    """
    检测危机状态
    """
    try:
        crisis_result = twin_engine.detect_crisis(patient_id)
        return {
            "success": True,
            "crisis_result": crisis_result.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"危机检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@twin_router.post("/simulate-treatment/{patient_id}")
async def simulate_treatment(
    patient_id: str,
    treatment_plan: Dict[str, Any],
    duration_hours: float = 168
):
    """
    模拟治疗效果
    """
    try:
        simulation = twin_engine.simulate_treatment(patient_id, treatment_plan, duration_hours)
        return {
            "success": True,
            "simulation": simulation.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"治疗模拟失败: {e}")
        raise HTTPException(status_code=500, detail=f"模拟失败: {str(e)}")

@twin_router.get("/insights/{patient_id}")
async def get_twin_insights(
    patient_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    """
    获取数字孪生洞察
    """
    try:
        time_range = None
        if start_time or end_time:
            time_range = {"start": start_time, "end": end_time}
        
        insights = twin_engine.get_twin_insights(patient_id, time_range)
        return {
            "success": True,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取洞察失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取洞察失败: {str(e)}")

@twin_router.get("/export/{patient_id}")
async def export_twin_data(patient_id: str):
    """
    导出数字孪生数据
    """
    try:
        export_data = twin_engine.export_twin_data(patient_id)
        return {
            "success": True,
            "export_data": export_data,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"导出数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@twin_router.get("/evolution-patterns/{patient_id}")
async def get_evolution_patterns(patient_id: str):
    """
    获取演化模式
    """
    try:
        if patient_id not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail="患者数字孪生不存在")
        
        twin = twin_engine.patient_twins[patient_id]
        return {
            "success": True,
            "evolution_patterns": twin.evolution_patterns,
            "treatment_effectiveness": twin.treatment_effectiveness,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取演化模式失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取模式失败: {str(e)}")

@twin_router.get("/treatment-effectiveness/{patient_id}")
async def get_treatment_effectiveness(patient_id: str):
    """
    获取治疗效果数据
    """
    try:
        if patient_id not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail="患者数字孪生不存在")
        
        twin = twin_engine.patient_twins[patient_id]
        return {
            "success": True,
            "treatment_effectiveness": twin.treatment_effectiveness,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取治疗效果失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取效果失败: {str(e)}")

@twin_router.post("/batch-update")
async def batch_update_twins(update_requests: List[TwinUpdateRequest]):
    """
    批量更新数字孪生状态
    """
    try:
        results = []
        failed = []
        
        for i, update_request in enumerate(update_requests):
            try:
                twin = twin_engine.update_twin_state(update_request)
                results.append({
                    "patient_id": update_request.patient_id,
                    "success": True,
                    "twin_version": twin.twin_version
                })
            except Exception as e:
                results.append({
                    "patient_id": update_request.patient_id,
                    "success": False,
                    "error": str(e)
                })
                failed.append(update_request.patient_id)
        
        return {
            "success": True,
            "total_requests": len(update_requests),
            "successful_updates": len([r for r in results if r["success"]]),
            "failed_updates": len(failed),
            "results": results,
            "failed_patients": failed,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"批量更新失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量更新失败: {str(e)}")

@twin_router.get("/comparison/{patient_id1}/{patient_id2}")
async def compare_twins(patient_id1: str, patient_id2: str):
    """
    比较两个患者的数字孪生状态
    """
    try:
        if patient_id1 not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail=f"患者 {patient_id1} 的数字孪生不存在")
        
        if patient_id2 not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail=f"患者 {patient_id2} 的数字孪生不存在")
        
        twin1 = twin_engine.patient_twins[patient_id1]
        twin2 = twin_engine.patient_twins[patient_id2]
        
        comparison = {
            "patient1": {
                "id": patient_id1,
                "stability_score": twin1.current_state.stability_score,
                "state_type": twin1.current_state.state_type,
                "emotion_type": twin1.current_state.emotional_state.emotion_type if twin1.current_state.emotional_state else None,
                "last_updated": twin1.updated_at.isoformat()
            },
            "patient2": {
                "id": patient_id2,
                "stability_score": twin2.current_state.stability_score,
                "state_type": twin2.current_state.state_type,
                "emotion_type": twin2.current_state.emotional_state.emotion_type if twin2.current_state.emotional_state else None,
                "last_updated": twin2.updated_at.isoformat()
            },
            "comparison": {
                "stability_difference": twin1.current_state.stability_score - twin2.current_state.stability_score,
                "similarity_score": 1.0 - abs(twin1.current_state.stability_score - twin2.current_state.stability_score)
            }
        }
        
        return {
            "success": True,
            "comparison": comparison,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"比较数字孪生失败: {e}")
        raise HTTPException(status_code=500, detail=f"比较失败: {str(e)}")

@twin_router.get("/health")
async def digital_twin_health():
    """
    数字孪生系统健康检查
    """
    try:
        health_status = {
            "status": "healthy",
            "models_initialized": twin_engine.models_initialized,
            "active_twins": len(twin_engine.patient_twins),
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
    except Exception as e:
        logger.error(f"数字孪生系统健康检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")

@twin_router.delete("/{patient_id}")
async def delete_patient_twin(patient_id: str):
    """
    删除患者数字孪生
    """
    try:
        if patient_id not in twin_engine.patient_twins:
            raise HTTPException(status_code=404, detail="患者数字孪生不存在")
        
        del twin_engine.patient_twins[patient_id]
        
        return {
            "success": True,
            "message": f"患者 {patient_id} 的数字孪生已删除",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除数字孪生失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@twin_router.get("/list")
async def list_patient_twins():
    """
    列出所有数字孪生
    """
    try:
        twin_list = []
        for patient_id, twin in twin_engine.patient_twins.items():
            twin_list.append({
                "patient_id": patient_id,
                "twin_version": twin.twin_version,
                "stability_score": twin.current_state.stability_score,
                "state_type": twin.current_state.state_type,
                "last_updated": twin.updated_at.isoformat()
            })
        
        return {
            "success": True,
            "twins": twin_list,
            "total_count": len(twin_list),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"列出数字孪生失败: {e}")
        raise HTTPException(status_code=500, detail=f"列出失败: {str(e)}")