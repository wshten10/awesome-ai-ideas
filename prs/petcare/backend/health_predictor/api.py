"""
Health Predictor - REST API endpoints.
"""
from datetime import datetime, date, timedelta
from uuid import UUID
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from backend.database.session import get_db
from backend.database.models import Pet, ActivityLog, DietLog, HealthAlert
from backend.health_predictor.models import (
    RiskAssessmentRequest, RiskAssessmentResponse, RiskFactor,
    TrendAnalysisRequest, TrendAnalysisResponse, TrendAnalysis, TrendDataPoint,
    AlertConfig, AlertResponse,
)
from backend.health_predictor.engine import risk_engine, trend_analyzer, alert_engine

router = APIRouter()


async def _get_pet_or_404(db: AsyncSession, pet_id: UUID):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


def _row_to_dict(row):
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


@router.post("/risk-assessment", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest, db: AsyncSession = Depends(get_db)):
    """Perform comprehensive health risk assessment."""
    pet = await _get_pet_or_404(db, request.pet_id)
    cutoff = datetime.utcnow() - timedelta(days=request.period_days)

    weight_history = []
    if request.include_weight_trend:
        # Simulated weight history from pet profile
        if pet.weight:
            for i in range(request.period_days):
                weight_history.append({"date": (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d"),
                                        "value": pet.weight + (i - request.period_days/2) * 0.01})

    activity_history = []
    if request.include_activity_trend:
        stmt = select(ActivityLog).where(and_(ActivityLog.pet_id == request.pet_id, ActivityLog.recorded_at >= cutoff))
        result = await db.execute(stmt)
        activity_history = [_row_to_dict(l) for l in result.scalars().all()]

    diet_history = []
    if request.include_diet_analysis:
        stmt = select(DietLog).where(and_(DietLog.pet_id == request.pet_id, DietLog.logged_at >= cutoff))
        result = await db.execute(stmt)
        diet_history = [_row_to_dict(l) for l in result.scalars().all()]

    pet_data = {"weight_history": weight_history, "activity_history": activity_history, "diet_history": diet_history}
    assessment = risk_engine.assess_risk(pet_data, request.period_days)

    # Create alerts for high-risk factors
    alerts = alert_engine.generate_alerts(str(request.pet_id), assessment)
    for alert_data in alerts:
        alert = HealthAlert(pet_id=request.pet_id, alert_type=alert_data["alert_type"],
                           severity=alert_data["severity"], title=alert_data["title"],
                           description=alert_data["description"], recommendation=alert_data.get("recommendation"),
                           risk_score=alert_data.get("risk_score"))
        db.add(alert)
    if alerts:
        await db.commit()

    return RiskAssessmentResponse(
        pet_id=request.pet_id, assessment_id=assessment["assessment_id"],
        timestamp=assessment["timestamp"], overall_risk_score=assessment["overall_risk_score"],
        risk_level=assessment["risk_level"],
        risk_factors=[RiskFactor(**f) for f in assessment["risk_factors"]],
        trend_analysis=assessment["trend_analysis"],
        recommendations=assessment["recommendations"],
        next_assessment_date=assessment["next_assessment_date"],
    )


@router.post("/trend-analysis", response_model=TrendAnalysisResponse)
async def analyze_trends(request: TrendAnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Analyze health metric trends over time."""
    await _get_pet_or_404(db, request.pet_id)
    cutoff = datetime.utcnow() - timedelta(days=request.period_days)

    trends = []
    if request.metric == "weight":
        # Use simulated weight data from pet profile
        stmt = select(Pet).where(Pet.id == request.pet_id)
        result = await db.execute(stmt)
        pet = result.scalar_one_or_none()
        if pet and pet.weight:
            data = [{"date": (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d"),
                      "value": pet.weight + (i - request.period_days/2) * 0.01}
                     for i in range(min(request.period_days, 30))]
            trends.append(trend_analyzer.analyze_metric(data, "weight", "kg"))
    elif request.metric == "activity":
        stmt = select(ActivityLog).where(and_(ActivityLog.pet_id == request.pet_id, ActivityLog.recorded_at >= cutoff))
        result = await db.execute(stmt)
        logs = [_row_to_dict(l) for l in result.scalars().all()]
        data = [{"date": l["recorded_at"].strftime("%Y-%m-%d"), "value": l.get("duration_minutes", 0) or 0} for l in logs]
        trends.append(trend_analyzer.analyze_metric(data, "activity_duration", "minutes"))
    elif request.metric == "calories":
        stmt = select(DietLog).where(and_(DietLog.pet_id == request.pet_id, DietLog.logged_at >= cutoff))
        result = await db.execute(stmt)
        logs = [_row_to_dict(l) for l in result.scalars().all()]
        data = [{"date": l["logged_at"].strftime("%Y-%m-%d"), "value": l.get("calories", 0) or 0} for l in logs]
        trends.append(trend_analyzer.analyze_metric(data, "calorie_intake", "kcal"))

    insights = [f"Analyzed {request.metric} over {request.period_days} days"]
    for t in trends:
        if t["is_concerning"]:
            insights.append(f"⚠️ {t['metric_name']} shows concerning {t['trend_direction']} trend")

    return TrendAnalysisResponse(
        pet_id=request.pet_id, trends=[TrendAnalysis(**t) for t in trends],
        correlations=[], insights=insights,
    )


@router.get("/alerts/{pet_id}", response_model=List[AlertResponse])
async def get_alerts(
    pet_id: UUID, severity: Optional[str] = None, limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get health alerts for a pet."""
    await _get_pet_or_404(db, pet_id)
    stmt = select(HealthAlert).where(HealthAlert.pet_id == pet_id).order_by(HealthAlert.created_at.desc()).limit(limit)
    if severity:
        stmt = stmt.where(HealthAlert.severity == severity)
    result = await db.execute(stmt)
    alerts = result.scalars().all()
    return [AlertResponse(alert_id=str(a.id), pet_id=a.pet_id, alert_type=a.alert_type,
                          severity=a.severity, title=a.title, description=a.description,
                          recommendation=a.recommendation, risk_score=a.risk_score,
                          created_at=a.created_at, is_dismissed=a.is_dismissed) for a in alerts]


@router.put("/alerts/{alert_id}/dismiss")
async def dismiss_alert(alert_id: UUID, db: AsyncSession = Depends(get_db)):
    """Dismiss a health alert."""
    from sqlalchemy import select
    result = await db.execute(select(HealthAlert).where(HealthAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_dismissed = True
    await db.commit()
    return {"status": "dismissed", "alert_id": str(alert_id)}
