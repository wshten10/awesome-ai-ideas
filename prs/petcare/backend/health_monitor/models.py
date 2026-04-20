"""
Health Monitor - Pydantic models for health monitoring.
"""
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class BehaviorType(str, Enum):
    NORMAL = "normal"
    EATING = "eating"
    DRINKING = "drinking"
    SLEEPING = "sleeping"
    PLAYING = "playing"
    WALKING = "walking"
    RUNNING = "running"
    GROOMING = "grooming"
    BARKING = "barking"
    SCRATCHING = "scratching"
    LIMPING = "limping"
    PANTING = "panting"
    HIDING = "hiding"
    AGGRESSIVE = "aggressive"
    LETHARGIC = "lethargic"
    VOMITING = "vomiting"
    OTHER = "other"


class SoundEventType(str, Enum):
    BARK = "bark"
    MEOW = "meow"
    WHINE = "whine"
    GROWL = "growl"
    COUGH = "cough"
    SNEEZE = "sneeze"
    WHEEZE = "wheeze"
    VOMIT_SOUND = "vomit_sound"
    PANT = "pant"
    CRY = "cry"
    NORMAL = "normal"
    UNKNOWN = "unknown"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LOW = "low"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class CameraAnalysisRequest(BaseModel):
    pet_id: UUID
    image_data: str = Field(..., description="Base64 encoded image data")
    image_format: str = Field(default="jpeg")
    timestamp: Optional[datetime] = None


class BehaviorDetection(BaseModel):
    behavior_type: BehaviorType
    confidence: float = Field(ge=0.0, le=1.0)
    bounding_box: Optional[Dict[str, float]] = None
    pose_keypoints: Optional[List[Dict[str, float]]] = None
    emotional_state: Optional[str] = None


class CameraAnalysisResponse(BaseModel):
    pet_id: UUID
    analysis_id: str
    timestamp: datetime
    behaviors: List[BehaviorDetection]
    body_condition_score: Optional[float] = Field(None, ge=1.0, le=9.0)
    posture_quality: Optional[str] = None
    coat_condition: Optional[str] = None
    anomalies_detected: List[str] = Field(default_factory=list)


class SoundAnalysisRequest(BaseModel):
    pet_id: UUID
    audio_data: str = Field(..., description="Base64 encoded audio data")
    audio_format: str = Field(default="wav")
    duration_seconds: float = Field(gt=0.0, le=60.0)
    timestamp: Optional[datetime] = None


class SoundEvent(BaseModel):
    event_type: SoundEventType
    confidence: float = Field(ge=0.0, le=1.0)
    start_time: float
    end_time: float
    frequency_hz: Optional[float] = None
    amplitude_db: Optional[float] = None
    is_abnormal: bool = False


class SoundAnalysisResponse(BaseModel):
    pet_id: UUID
    analysis_id: str
    timestamp: datetime
    events: List[SoundEvent]
    overall_stress_level: float = Field(ge=0.0, le=1.0)
    respiratory_pattern: Optional[str] = None
    health_indicators: List[str] = Field(default_factory=list)


class ActivityLogRequest(BaseModel):
    pet_id: UUID
    activity_type: str
    duration_minutes: Optional[float] = None
    distance_meters: Optional[float] = None
    steps: Optional[int] = None
    calories_burned: Optional[float] = None
    heart_rate: Optional[int] = Field(None, ge=30, le=300)
    timestamp: Optional[datetime] = None


class ActivitySummary(BaseModel):
    pet_id: UUID
    date: str
    total_duration_minutes: float
    total_distance_meters: float
    total_steps: int
    total_calories: float
    activity_level: ActivityLevel
    activity_breakdown: Dict[str, float]
    hourly_distribution: Dict[str, float]
    comparison_with_average: Optional[Dict[str, float]] = None


class DietLogRequest(BaseModel):
    pet_id: UUID
    meal_type: str
    food_name: str
    food_brand: Optional[str] = None
    amount_grams: Optional[float] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None
    water_intake_ml: Optional[float] = None
    timestamp: Optional[datetime] = None


class DietSummary(BaseModel):
    pet_id: UUID
    date: str
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    total_water_ml: float
    meal_count: int
    nutritional_balance_score: float = Field(ge=0.0, le=1.0)
    recommendations: List[str] = Field(default_factory=list)


class HealthOverview(BaseModel):
    pet_id: UUID
    overall_health_score: float = Field(ge=0.0, le=1.0)
    behavior_health: float
    diet_health: float
    activity_health: float
    recent_anomalies: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    last_updated: datetime
