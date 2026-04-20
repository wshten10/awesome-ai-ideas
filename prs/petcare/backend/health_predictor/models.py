"""
Health Predictor - Pydantic models.
"""
from datetime import datetime, date
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class RiskAssessmentRequest(BaseModel):
    pet_id: UUID
    include_weight_trend: bool = True
    include_activity_trend: bool = True
    include_diet_analysis: bool = True
    period_days: int = Field(default=30, ge=7, le=365)


class RiskFactor(BaseModel):
    factor_name: str
    risk_level: str  # low, medium, high
    score: float = Field(ge=0.0, le=1.0)
    description: str
    contributing_data: Dict[str, Any] = Field(default_factory=dict)


class RiskAssessmentResponse(BaseModel):
    pet_id: UUID
    assessment_id: str
    timestamp: datetime
    overall_risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: str
    risk_factors: List[RiskFactor]
    trend_analysis: Dict[str, Any]
    recommendations: List[str]
    next_assessment_date: date


class TrendDataPoint(BaseModel):
    date: str
    value: float
    baseline: Optional[float] = None


class TrendAnalysis(BaseModel):
    metric_name: str
    unit: str
    current_value: float
    trend_direction: str  # increasing, decreasing, stable
    trend_slope: float
    data_points: List[TrendDataPoint]
    anomaly_count: int
    is_concerning: bool


class TrendAnalysisRequest(BaseModel):
    pet_id: UUID
    metric: str  # weight, activity, calories, water_intake
    period_days: int = Field(default=30, ge=7, le=365)


class TrendAnalysisResponse(BaseModel):
    pet_id: UUID
    trends: List[TrendAnalysis]
    correlations: List[Dict[str, Any]]
    insights: List[str]


class AlertConfig(BaseModel):
    pet_id: UUID
    alert_types: List[str] = Field(default_factory=lambda: ["weight_change", "behavior_anomaly", "diet_change", "risk_prediction"])
    severity_threshold: str = Field(default="medium")
    notify_channels: List[str] = Field(default_factory=lambda: ["in_app"])


class AlertResponse(BaseModel):
    alert_id: str
    pet_id: UUID
    alert_type: str
    severity: str
    title: str
    description: str
    recommendation: Optional[str] = None
    risk_score: Optional[float] = None
    created_at: datetime
    is_dismissed: bool = False
