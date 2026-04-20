"""
治疗环境数据模型
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class EnvironmentType(str, Enum):
    """环境类型"""
    VR = "vr"
    AR = "ar"
    PHYSICAL = "physical"
    HYBRID = "hybrid"

class SessionStatus(str, Enum):
    """会话状态"""
    SCHEDULED = "scheduled"
    PREPARING = "preparing"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"

class TherapyType(str, Enum):
    """治疗类型"""
    EXPOSURE_THERAPY = "exposure_therapy"
    COGNITIVE_BEHAVIORAL = "cognitive_behavioral"
    MINDFULNESS = "mindfulness"
    EMOTION_REGULATION = "emotion_regulation"
    SOCIAL_SKILLS = "social_skills"
    VR_REHABILITATION = "vr_rehabilitation"

class VRSceneType(str, Enum):
    """VR场景类型"""
    RELAXATION_GARDEN = "relaxation_garden"
    BEACH_PARADISE = "beach_paradise"
    MOUNTAIN_RETREAT = "mountain_retreat"
    FOREST_WALK = "forest_walk"
    COSMIC_JOURNEY = "cosmic_journey"
    UNDERWORLD = "underworld"
    CUSTOM_SCENE = "custom_scene"

class AROverlayType(str, Enum):
    """AR覆盖类型"""
    EMOTION_INDICATORS = "emotion_indicators"
    TREATING_GUIDE = "treating_guide"
    PROGRESS_MONITOR = "progress_monitor"
    SOCIAL_ASSISTANT = "social_assistant"
    EDUCATIONAL_OVERLAY = "educational_overlay"

class EnvironmentConfig(BaseModel):
    """环境配置"""
    environment_type: EnvironmentType
    therapy_type: TherapyType
    scene_config: Dict[str, Any] = Field(default_factory=dict)
    interaction_modes: List[str] = Field(default_factory=list)
    accessibility_features: List[str] = Field(default_factory=list)
    custom_parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class SessionData(BaseModel):
    """会话数据"""
    session_id: str
    patient_id: str
    therapist_id: str
    environment_type: EnvironmentType
    therapy_type: TherapyType
    
    # 时间信息
    scheduled_start: datetime
    actual_start: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_planned: Optional[float] = None
    duration_actual: Optional[float] = None
    
    # 状态信息
    status: SessionStatus
    progress: float = Field(..., ge=0.0, le=1.0)
    
    # 环境数据
    environment_config: EnvironmentConfig
    session_parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # 情感和行为数据
    emotion_data: Dict[str, Any] = Field(default_factory=dict)
    behavior_data: Dict[str, Any] = Field(default_factory=dict)
    
    # 治疗数据
    treatment_goals: List[str] = Field(default_factory=list)
    interventions_applied: List[str] = Field(default_factory=list)
    patient_feedback: Dict[str, Any] = Field(default_factory=dict)
    
    # 技术数据
    device_info: Dict[str, Any] = Field(default_factory=dict)
    network_metrics: Dict[str, Any] = Field(default_factory=dict)
    error_log: List[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class VRSession(SessionData):
    """VR治疗会话"""
    scene_type: VRSceneType
    vr_parameters: Dict[str, Any] = Field(default_factory=dict)
    interaction_data: List[Dict[str, Any]] = Field(default_factory=list)
    presence_metrics: Dict[str, float] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

class ARSession(SessionData):
    """AR治疗会话"""
    overlay_types: List[AROverlayType] = Field(default_factory=list)
    ar_parameters: Dict[str, Any] = Field(default_factory=dict)
    spatial_data: Dict[str, Any] = Field(default_factory=dict)
    real_world_integration: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

class PhysicalSession(SessionData):
    """物理环境治疗会话"""
    physical_space_config: Dict[str, Any] = Field(default_factory=dict)
    sensor_data: Dict[str, Any] = Field(default_factory=dict)
    environmental_factors: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

class SessionMetrics(BaseModel):
    """会话指标"""
    session_id: str
    engagement_level: float = Field(..., ge=0.0, le=1.0)
    emotional_regulation: float = Field(..., ge=0.0, le=1.0)
    learning_progress: float = Field(..., ge=0.0, le=1.0)
    comfort_level: float = Field(..., ge=0.0, le=1.0)
    technical_performance: float = Field(..., ge=0.0, le=1.0)
    
    # 时间指标
    session_duration: float
    active_time_percentage: float
    
    # 交互指标
    interaction_count: int
    response_time_avg: float
    error_rate: float
    
    # 情感指标
    emotion_stability: float
    stress_reduction: float
    positive_emotion_increase: float
    
    created_at: datetime = Field(default_factory=datetime.now)

class TherapyEnvironmentRequest(BaseModel):
    """治疗环境请求"""
    patient_id: str
    therapist_id: str
    environment_type: EnvironmentType
    therapy_type: TherapyType
    scene_config: Optional[Dict[str, Any]] = None
    session_parameters: Optional[Dict[str, Any]] = None
    treatment_goals: Optional[List[str]] = None
    
    class Config:
        use_enum_values = True

class EnvironmentSimulationResult(BaseModel):
    """环境模拟结果"""
    simulation_id: str
    original_config: EnvironmentConfig
    simulated_outcomes: Dict[str, Any]
    recommended_changes: List[str] = Field(default_factory=list)
    confidence_level: float = Field(..., ge=0.0, le=1.0)
    simulation_time: datetime = Field(default_factory=datetime.now)

class EnvironmentProfile(BaseModel):
    """环境档案"""
    profile_id: str
    name: str
    description: str
    environment_type: EnvironmentType
    therapy_type: TherapyType
    target_conditions: List[str] = Field(default_factory=list)
    effectiveness_rating: float = Field(..., ge=0.0, le=1.0)
    usage_count: int = 0
    last_used: Optional[datetime] = None
    customization_options: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

class SessionSummary(BaseModel):
    """会话摘要"""
    session_id: str
    patient_id: str
    therapist_id: str
    environment_type: EnvironmentType
    therapy_type: TherapyType
    duration: float
    status: SessionStatus
    key_achievements: List[str] = Field(default_factory=list)
    challenges_encountered: List[str] = Field(default_factory=list)
    next_session_recommendations: List[str] = Field(default_factory=list)
    overall_satisfaction: float = Field(..., ge=0.0, le=1.0)
    
    class Config:
        use_enum_values = True