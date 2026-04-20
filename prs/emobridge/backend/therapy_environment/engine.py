"""
治疗环境引擎
沉浸式治疗环境核心系统
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import uuid
from .models import (
    VRSession, ARSession, PhysicalSession, EnvironmentConfig, EnvironmentType,
    TherapyType, SessionStatus, TherapyEnvironmentRequest, SessionMetrics,
    EnvironmentSimulationResult, EnvironmentProfile, SessionSummary
)

logger = logging.getLogger(__name__)

class TherapyEnvironmentEngine:
    """治疗环境引擎主类"""
    
    def __init__(self):
        """初始化治疗环境引擎"""
        self.active_sessions: Dict[str, SessionData] = {}
        self.completed_sessions: Dict[str, SessionData] = {}
        self.environment_profiles: Dict[str, EnvironmentProfile] = {}
        self.initialize_default_profiles()
    
    def initialize_default_profiles(self):
        """初始化默认环境档案"""
        # 放松花园场景
        relaxation_garden = EnvironmentProfile(
            profile_id="relaxation_garden",
            name="放松花园",
            description="宁静的虚拟花园，适合放松和冥想",
            environment_type=EnvironmentType.VR,
            therapy_type=TherapyType.MINDFULNESS,
            target_conditions=["焦虑", "压力", "失眠"],
            effectiveness_rating=0.85,
            customization_options={
                "ambient_sounds": ["birds", "water", "wind"],
                "visual_elements": ["flowers", "trees", "water_fountain"],
                "lighting": "natural",
                "time_of_day": "dawn"
            }
        )
        
        # 海滩天堂场景
        beach_paradise = EnvironmentProfile(
            profile_id="beach_paradise",
            name="海滩天堂",
            description="热带海滩场景，用于暴露疗法和情感调节",
            environment_type=EnvironmentType.VR,
            therapy_type=TherapyType.EXPOSURE_THERAPY,
            target_conditions=["恐惧症", "社交焦虑", "创伤后应激障碍"],
            effectiveness_rating=0.80,
            customization_options={
                "ocean_waves": "gentle",
                "beach_elements": ["sand", "palm_trees", "blue_sky"],
                "weather": "sunny",
                "time_of_day": "afternoon"
            }
        )
        
        # 森林漫步场景
        forest_walk = EnvironmentProfile(
            profile_id="forest_walk",
            description="宁静的森林小径，适合正念行走和情绪调节",
            environment_type=EnvironmentType.VR,
            therapy_type=TherapyType.MINDFULNESS,
            target_conditions=["抑郁", "焦虑", "注意力不集中"],
            effectiveness_rating=0.82,
            customization_options={
                "forest_type": "deciduous",
                "path_elements": ["stones", "fallen_leaves", "moss"],
                "wildlife_sounds": ["birds", "insects"],
                "season": "autumn"
            }
        )
        
        # 添加到环境档案
        self.environment_profiles[relaxation_garden.profile_id] = relaxation_garden
        self.environment_profiles[beach_paradise.profile_id] = beach_paradise
        self.environment_profiles[forest_walk.profile_id] = forest_walk
        
        logger.info(f"初始化了 {len(self.environment_profiles)} 个默认环境档案")
    
    def create_session(self, request: TherapyEnvironmentRequest) -> SessionData:
        """创建治疗会话"""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # 创建环境配置
        config = EnvironmentConfig(
            environment_type=request.environment_type,
            therapy_type=request.therapy_type,
            scene_config=request.scene_config or {},
            custom_parameters=request.session_parameters or {}
        )
        
        # 根据环境类型创建具体会话
        if request.environment_type == EnvironmentType.VR:
            session = VRSession(
                session_id=session_id,
                patient_id=request.patient_id,
                therapist_id=request.therapist_id,
                environment_type=request.environment_type,
                therapy_type=request.therapy_type,
                scheduled_start=datetime.now() + timedelta(minutes=5),  # 默认5分钟后开始
                status=SessionStatus.SCHEDULED,
                progress=0.0,
                environment_config=config,
                treatment_goals=request.treatment_goals or []
            )
        
        elif request.environment_type == EnvironmentType.AR:
            session = ARSession(
                session_id=session_id,
                patient_id=request.patient_id,
                therapist_id=request.therapist_id,
                environment_type=request.environment_type,
                therapy_type=request.therapy_type,
                scheduled_start=datetime.now() + timedelta(minutes=5),
                status=SessionStatus.SCHEDULED,
                progress=0.0,
                environment_config=config,
                treatment_goals=request.treatment_goals or []
            )
        
        else:  # PHYSICAL
            session = PhysicalSession(
                session_id=session_id,
                patient_id=request.patient_id,
                therapist_id=request.therapist_id,
                environment_type=request.environment_type,
                therapy_type=request.therapy_type,
                scheduled_start=datetime.now() + timedelta(minutes=5),
                status=SessionStatus.SCHEDULED,
                progress=0.0,
                environment_config=config,
                treatment_goals=request.treatment_goals or []
            )
        
        # 添加到活跃会话
        self.active_sessions[session_id] = session
        
        logger.info(f"创建治疗会话: {session_id}, 患者: {request.patient_id}")
        
        return session
    
    def start_session(self, session_id: str) -> SessionData:
        """开始治疗会话"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        if session.status != SessionStatus.SCHEDULED:
            raise ValueError(f"会话 {session_id} 状态错误，无法开始")
        
        # 更新会话状态
        session.status = SessionStatus.ACTIVE
        session.actual_start = datetime.now()
        session.updated_at = datetime.now()
        
        # 初始化环境参数
        self._initialize_environment_parameters(session)
        
        logger.info(f"开始治疗会话: {session_id}")
        
        return session
    
    def update_session_progress(self, session_id: str, progress_data: Dict[str, Any]) -> SessionData:
        """更新会话进度"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        # 更新进度
        session.progress = progress_data.get("progress", session.progress)
        
        # 更新情感数据
        if "emotion_data" in progress_data:
            session.emotion_data.update(progress_data["emotion_data"])
        
        # 更新行为数据
        if "behavior_data" in progress_data:
            session.behavior_data.update(progress_data["behavior_data"])
        
        # 更新治疗应用
        if "interventions_applied" in progress_data:
            session.interventions_applied.extend(progress_data["interventions_applied"])
        
        # 更新患者反馈
        if "patient_feedback" in progress_data:
            session.patient_feedback.update(progress_data["patient_feedback"])
        
        session.updated_at = datetime.now()
        
        # 检查是否完成
        if session.progress >= 1.0:
            session.status = SessionStatus.COMPLETED
            session.end_time = datetime.now()
            session.duration_actual = (session.end_time - session.actual_start).total_seconds() / 60
        
        logger.info(f"更新会话进度: {session_id}, 进度: {session.progress:.1%}")
        
        return session
    
    def complete_session(self, session_id: str, completion_data: Dict[str, Any] = None) -> SessionData:
        """完成治疗会话"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        # 更新完成数据
        session.status = SessionStatus.COMPLETED
        session.end_time = datetime.now()
        session.duration_actual = (session.end_time - session.actual_start).total_seconds() / 60
        
        if completion_data:
            session.patient_feedback.update(completion_data.get("patient_feedback", {}))
            session.interventions_applied.extend(completion_data.get("interventions_applied", []))
        
        # 计算会话指标
        metrics = self._calculate_session_metrics(session)
        
        # 添加到已完成会话
        self.completed_sessions[session_id] = session
        del self.active_sessions[session_id]
        
        # 更新环境档案使用次数
        self._update_environment_profile_usage(session.environment_config.environment_type, session.environment_config.therapy_type)
        
        logger.info(f"完成治疗会话: {session_id}, 持续时间: {session.duration_actual:.1f}分钟")
        
        return session
    
    def pause_session(self, session_id: str, reason: str = "") -> SessionData:
        """暂停治疗会话"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        session.status = SessionStatus.PAUSED
        session.updated_at = datetime.now()
        
        logger.info(f"暂停治疗会话: {session_id}, 原因: {reason}")
        
        return session
    
    def resume_session(self, session_id: str) -> SessionData:
        """恢复治疗会话"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        if session.status != SessionStatus.PAUSED:
            raise ValueError(f"会话 {session_id} 状态错误，无法恢复")
        
        session.status = SessionStatus.ACTIVE
        session.updated_at = datetime.now()
        
        logger.info(f"恢复治疗会话: {session_id}")
        
        return session
    
    def cancel_session(self, session_id: str, reason: str = "") -> SessionData:
        """取消治疗会话"""
        if session_id not in self.active_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        session.status = SessionStatus.CANCELLED
        session.updated_at = datetime.now()
        
        # 移动到已完成会话
        self.completed_sessions[session_id] = session
        del self.active_sessions[session_id]
        
        logger.info(f"取消治疗会话: {session_id}, 原因: {reason}")
        
        return session
    
    def get_session_metrics(self, session_id: str) -> SessionMetrics:
        """获取会话指标"""
        if session_id not in self.active_sessions and session_id not in self.completed_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions.get(session_id, self.completed_sessions[session_id])
        
        metrics = self._calculate_session_metrics(session)
        
        return metrics
    
    def simulate_environment(self, config: EnvironmentConfig) -> EnvironmentSimulationResult:
        """模拟治疗效果"""
        simulation_id = f"sim_{uuid.uuid4().hex[:8]}"
        
        # 基于配置模拟治疗效果
        simulated_outcomes = self._simulate_treatment_outcomes(config)
        
        # 生成推荐
        recommended_changes = self._generate_environment_recommendations(config, simulated_outcomes)
        
        result = EnvironmentSimulationResult(
            simulation_id=simulation_id,
            original_config=config,
            simulated_outcomes=simulated_outcomes,
            recommended_changes=recommended_changes,
            confidence_level=self._calculate_simulation_confidence(config, simulated_outcomes)
        )
        
        logger.info(f"完成环境模拟: {simulation_id}")
        
        return result
    
    def get_environment_profiles(self, environment_type: Optional[EnvironmentType] = None, therapy_type: Optional[TherapyType] = None) -> List[EnvironmentProfile]:
        """获取环境档案"""
        profiles = list(self.environment_profiles.values())
        
        if environment_type:
            profiles = [p for p in profiles if p.environment_type == environment_type]
        
        if therapy_type:
            profiles = [p for p in profiles if p.therapy_type == therapy_type]
        
        return profiles
    
    def create_custom_profile(self, profile: EnvironmentProfile) -> EnvironmentProfile:
        """创建自定义环境档案"""
        # 验证档案名称
        if any(p.name == profile.name for p in self.environment_profiles.values()):
            raise ValueError(f"环境档案名称 '{profile.name}' 已存在")
        
        self.environment_profiles[profile.profile_id] = profile
        
        logger.info(f"创建自定义环境档案: {profile.profile_id}")
        
        return profile
    
    def get_active_sessions(self) -> List[SessionData]:
        """获取活跃会话"""
        return list(self.active_sessions.values())
    
    def get_patient_sessions(self, patient_id: str) -> List[SessionData]:
        """获取患者会话"""
        sessions = []
        
        # 活跃会话
        sessions.extend([s for s in self.active_sessions.values() if s.patient_id == patient_id])
        
        # 已完成会话
        sessions.extend([s for s in self.completed_sessions.values() if s.patient_id == patient_id])
        
        # 按时间排序
        sessions.sort(key=lambda x: x.created_at, reverse=True)
        
        return sessions
    
    def get_session_summary(self, session_id: str) -> SessionSummary:
        """获取会话摘要"""
        if session_id not in self.active_sessions and session_id not in self.completed_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions.get(session_id, self.completed_sessions[session_id])
        
        summary = SessionSummary(
            session_id=session_id,
            patient_id=session.patient_id,
            therapist_id=session.therapist_id,
            environment_type=session.environment_type,
            therapy_type=session.therapy_type,
            duration=session.duration_actual or 0,
            status=session.status,
            key_achievements=self._identify_key_achievements(session),
            challenges_encountered=self._identify_challenges(session),
            next_session_recommendations=self._generate_next_session_recommendations(session),
            overall_satisfaction=self._calculate_overall_satisfaction(session)
        )
        
        return summary
    
    def export_session_data(self, session_id: str) -> Dict[str, Any]:
        """导出会话数据"""
        if session_id not in self.active_sessions and session_id not in self.completed_sessions:
            raise ValueError(f"会话 {session_id} 不存在")
        
        session = self.active_sessions.get(session_id, self.completed_sessions[session_id])
        
        export_data = {
            "session_id": session_id,
            "patient_id": session.patient_id,
            "therapist_id": session.therapist_id,
            "environment_type": session.environment_type.value,
            "therapy_type": session.therapy_type.value,
            "status": session.status.value,
            "scheduled_start": session.scheduled_start.isoformat(),
            "actual_start": session.actual_start.isoformat() if session.actual_start else None,
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration_planned": session.duration_planned,
            "duration_actual": session.duration_actual,
            "progress": session.progress,
            "environment_config": session.environment_config.dict(),
            "treatment_goals": session.treatment_goals,
            "interventions_applied": session.interventions_applied,
            "patient_feedback": session.patient_feedback,
            "emotion_data": session.emotion_data,
            "behavior_data": session.behavior_data,
            "device_info": session.device_info,
            "error_log": session.error_log,
            "export_timestamp": datetime.now().isoformat()
        }
        
        return export_data
    
    def _initialize_environment_parameters(self, session: SessionData):
        """初始化环境参数"""
        # 根据环境类型设置默认参数
        if isinstance(session, VRSession):
            session.vr_parameters = {
                "render_quality": "high",
                "interaction_mode": "motion_controller",
                "haptic_feedback": True,
                "spatial_audio": True,
                "tracking_mode": "full_body"
            }
        
        elif isinstance(session, ARSession):
            session.ar_parameters = {
                "overlay_visibility": "full",
                "spatial_mapping": True,
                "hand_tracking": True,
                "voice_commands": True,
                "gesture_recognition": True
            }
        
        elif isinstance(session, PhysicalSession):
            session.physical_space_config = {
                "room_setup": "therapy_room",
                "lighting": "controlled",
                "temperature": "comfortable",
                "audio_system": "surround"
            }
    
    def _calculate_session_metrics(self, session: SessionData) -> SessionMetrics:
        """计算会话指标"""
        # 基础指标
        engagement_level = self._calculate_engagement(session)
        emotional_regulation = self._calculate_emotional_regulation(session)
        learning_progress = session.progress
        comfort_level = self._calculate_comfort_level(session)
        technical_performance = self._calculate_technical_performance(session)
        
        # 时间指标
        session_duration = session.duration_actual or 0
        active_time_percentage = self._calculate_active_time_percentage(session)
        
        # 交互指标
        interaction_count = len(session.interventions_applied)
        response_time_avg = self._calculate_average_response_time(session)
        error_rate = len(session.error_log) / max(1, interaction_count)
        
        # 情感指标
        emotion_stability = self._calculate_emotion_stability(session)
        stress_reduction = self._calculate_stress_reduction(session)
        positive_emotion_increase = self._calculate_positive_emotion_increase(session)
        
        return SessionMetrics(
            session_id=session_id,
            engagement_level=engagement_level,
            emotional_regulation=emotional_regulation,
            learning_progress=learning_progress,
            comfort_level=comfort_level,
            technical_performance=technical_performance,
            session_duration=session_duration,
            active_time_percentage=active_time_percentage,
            interaction_count=interaction_count,
            response_time_avg=response_time_avg,
            error_rate=error_rate,
            emotion_stability=emotion_stability,
            stress_reduction=stress_reduction,
            positive_emotion_increase=positive_emotion_increase,
            created_at=datetime.now()
        )
    
    def _simulate_treatment_outcomes(self, config: EnvironmentConfig) -> Dict[str, Any]:
        """模拟治疗效果"""
        # 基于配置参数模拟治疗效果
        outcomes = {
            "engagement_prediction": np.random.uniform(0.6, 0.9),
            "emotional_improvement": np.random.uniform(0.3, 0.8),
            "stress_reduction": np.random.uniform(0.2, 0.7),
            "comfort_score": np.random.uniform(0.5, 0.9),
            "technical_issues_probability": np.random.uniform(0.0, 0.2)
        }
        
        # 根据治疗类型调整模拟结果
        if config.therapy_type == TherapyType.MINDFULNESS:
            outcomes["emotional_improvement"] *= 1.2
            outcomes["stress_reduction"] *= 1.1
        elif config.therapy_type == TherapyType.EXPOSURE_THERAPY:
            outcomes["engagement_prediction"] *= 1.1
            outcomes["emotional_improvement"] *= 0.9
        
        return outcomes
    
    def _generate_environment_recommendations(self, config: EnvironmentConfig, outcomes: Dict[str, Any]) -> List[str]:
        """生成环境改进建议"""
        recommendations = []
        
        # 基于模拟结果生成建议
        if outcomes["engagement_prediction"] < 0.7:
            recommendations.append("增加交互性元素")
        
        if outcomes["emotional_improvement"] < 0.5:
            recommendations.append("调整环境氛围参数")
        
        if outcomes["technical_issues_probability"] > 0.15:
            recommendations.append("优化技术配置")
        
        # 基于环境类型的具体建议
        if config.environment_type == EnvironmentType.VR:
            recommendations.extend([
                "确保VR设备校准准确",
                "考虑添加视觉反馈元素",
                "优化场景光照设置"
            ])
        elif config.environment_type == EnvironmentType.AR:
            recommendations.extend([
                "确保AR空间映射准确",
                "优化手势识别设置",
                "考虑添加触觉反馈"
            ])
        
        return recommendations
    
    def _calculate_simulation_confidence(self, config: EnvironmentConfig, outcomes: Dict[str, Any]) -> float:
        """计算模拟置信度"""
        # 基于配置完整性和历史数据计算置信度
        confidence = 0.7
        
        # 检查配置完整性
        config_completeness = len(config.scene_config) / 10.0  # 假设10个参数为完整
        confidence += config_completeness * 0.2
        
        # 基于模拟结果一致性
        result_consistency = 1.0 - np.std(list(outcomes.values()))
        confidence += result_consistency * 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def _update_environment_profile_usage(self, environment_type: EnvironmentType, therapy_type: TherapyType):
        """更新环境档案使用次数"""
        for profile in self.environment_profiles.values():
            if profile.environment_type == environment_type and profile.therapy_type == therapy_type:
                profile.usage_count += 1
                profile.last_used = datetime.now()
                break
    
    def _calculate_engagement(self, session: SessionData) -> float:
        """计算参与度"""
        # 基于交互数量和情感变化计算参与度
        engagement = session.progress * 0.6
        engagement += len(session.interventions_applied) * 0.1
        engagement += min(1.0, len(session.emotion_data) / 10.0) * 0.3
        return min(1.0, engagement)
    
    def _calculate_emotional_regulation(self, session: SessionData) -> float:
        """计算情感调节能力"""
        # 基于情感稳定性变化
        if not session.emotion_data:
            return 0.5
        
        # 简化的情感稳定性计算
        emotion_values = [float(v.get('intensity', 0.5)) for v in session.emotion_data.values() if isinstance(v, dict)]
        
        if len(emotion_values) < 2:
            return 0.7
        
        # 计算情感波动
        volatility = np.std(emotion_values)
        regulation = 1.0 - volatility
        
        return max(0.0, min(1.0, regulation))
    
    def _calculate_comfort_level(self, session: SessionData) -> float:
        """计算舒适度"""
        if not session.patient_feedback:
            return 0.7
        
        comfort_score = 0.0
        feedback_count = 0
        
        for feedback in session.patient_feedback.values():
            if isinstance(feedback, dict) and 'comfort' in feedback:
                comfort_score += feedback['comfort']
                feedback_count += 1
        
        return comfort_score / max(1, feedback_count)
    
    def _calculate_technical_performance(self, session: SessionData) -> float:
        """计算技术性能"""
        error_rate = len(session.error_log) / max(1, len(session.interventions_applied))
        performance = 1.0 - error_rate
        return max(0.0, min(1.0, performance))
    
    def _calculate_active_time_percentage(self, session: SessionData) -> float:
        """计算活跃时间百分比"""
        if not session.actual_start:
            return 0.0
        
        total_time = (session.updated_at - session.actual_start).total_seconds()
        if total_time == 0:
            return 0.0
        
        active_time = session.progress * total_time
        return (active_time / total_time) * 100
    
    def _calculate_average_response_time(self, session: SessionData) -> float:
        """计算平均响应时间"""
        if not session.behavior_data or 'response_times' not in session.behavior_data:
            return 1.0  # 默认1秒
        
        response_times = session.behavior_data['response_times']
        if not response_times:
            return 1.0
        
        return sum(response_times) / len(response_times)
    
    def _calculate_emotion_stability(self, session: SessionData) -> float:
        """计算情感稳定性"""
        if not session.emotion_data:
            return 0.5
        
        # 计算情感强度的变化
        intensities = [float(v.get('intensity', 0.5)) for v in session.emotion_data.values() if isinstance(v, dict)]
        
        if len(intensities) < 2:
            return 0.7
        
        stability = 1.0 - np.std(intensities)
        return max(0.0, min(1.0, stability))
    
    def _calculate_stress_reduction(self, session: SessionData) -> float:
        """计算压力减少程度"""
        if not session.emotion_data:
            return 0.0
        
        # 查找压力相关的情感指标
        stress_indicators = ['anxiety', 'frustration', 'anger', 'stress']
        
        initial_stress = 0.0
        current_stress = 0.0
        
        for i, (key, value) in enumerate(session.emotion_data.items()):
            if isinstance(value, dict) and any(indicator in str(key).lower() for indicator in stress_indicators):
                stress_level = float(value.get('intensity', 0.5))
                if i < len(session.emotion_data) // 2:
                    initial_stress += stress_level
                else:
                    current_stress += stress_level
        
        if initial_stress == 0:
            return 0.5
        
        reduction = max(0.0, (initial_stress - current_stress) / initial_stress)
        return min(1.0, reduction)
    
    def _calculate_positive_emotion_increase(self, session: SessionData) -> float:
        """计算积极情感增加程度"""
        if not session.emotion_data:
            return 0.0
        
        positive_emotions = ['happy', 'joy', 'calm', 'relaxed']
        
        initial_positive = 0.0
        current_positive = 0.0
        
        for i, (key, value) in enumerate(session.emotion_data.items()):
            if isinstance(value, dict) and any(emotion in str(key).lower() for emotion in positive_emotions):
                positive_level = float(value.get('intensity', 0.5))
                if i < len(session.emotion_data) // 2:
                    initial_positive += positive_level
                else:
                    current_positive += positive_level
        
        if initial_positive == 0:
            return 0.5
        
        increase = max(0.0, (current_positive - initial_positive) / max(initial_positive, 1.0))
        return min(1.0, increase)
    
    def _identify_key_achievements(self, session: SessionData) -> List[str]:
        """识别关键成就"""
        achievements = []
        
        if session.progress >= 0.8:
            achievements.append("完成主要治疗目标")
        
        if len(session.interventions_applied) > 5:
            achievements.append("积极参与治疗过程")
        
        if session.patient_feedback.get('satisfaction', 0) > 0.8:
            achievements.append("患者满意度高")
        
        if len(session.error_log) == 0:
            achievements.append("技术运行稳定")
        
        return achievements
    
    def _identify_challenges(self, session: SessionData) -> List[str]:
        """识别挑战"""
        challenges = []
        
        if session.progress < 0.5:
            challenges.append("治疗进度缓慢")
        
        if len(session.error_log) > 3:
            challenges.append("技术问题较多")
        
        if session.patient_feedback.get('comfort', 0) < 0.5:
            challenges.append("患者舒适度较低")
        
        if session.emotion_data.get('negative_emotion_count', 0) > 3:
            challenges.append("情感调节存在困难")
        
        return challenges
    
    def _generate_next_session_recommendations(self, session: SessionData) -> List[str]:
        """生成下次会话建议"""
        recommendations = []
        
        if session.progress < 0.8:
            recommendations.append("增加治疗时间或频率")
        
        if len(session.interventions_applied) < 3:
            recommendations.append("增加更多交互式练习")
        
        if session.patient_feedback.get('satisfaction', 0) < 0.7:
            recommendations.append("调整环境设置以提高满意度")
        
        if session.emotion_data.get('negative_emotion_count', 0) > 2:
            recommendations.append("加强情感支持和调节训练")
        
        return recommendations
    
    def _calculate_overall_satisfaction(self, session: SessionData) -> float:
        """计算总体满意度"""
        if not session.patient_feedback:
            return 0.7
        
        # 计算各项满意度的平均值
        satisfaction_components = [
            session.patient_feedback.get('comfort', 0.5),
            session.patient_feedback.get('engagement', 0.5),
            session.patient_feedback.get('effectiveness', 0.5),
            session.patient_feedback.get('ease_of_use', 0.5),
            session.patient_feedback.get('overall_satisfaction', 0.5)
        ]
        
        valid_components = [s for s in satisfaction_components if s > 0]
        if not valid_components:
            return 0.5
        
        return sum(valid_components) / len(valid_components)