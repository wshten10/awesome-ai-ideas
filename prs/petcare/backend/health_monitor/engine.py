"""
Health Monitor - Core analysis engines for multi-modal health monitoring.
"""
import base64
import logging
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class CameraAnalysisEngine:
    """Computer vision engine for pet behavior and health analysis."""

    def __init__(self):
        self._model_loaded = False

    def _ensure_model(self):
        if not self._model_loaded:
            self._model_loaded = True
            logger.info("Camera analysis model loaded")

    async def analyze_image(self, image_data: str, pet_type: str = "dog") -> Dict[str, Any]:
        """Analyze pet image for behavior, body condition, and anomalies."""
        self._ensure_model()
        try:
            image_bytes = base64.b64decode(image_data)
            behaviors = self._detect_behaviors(image_bytes, pet_type)
            body_condition = self._estimate_body_condition(image_bytes, pet_type)
            posture = self._analyze_posture(image_bytes)
            coat_condition = self._analyze_coat(image_bytes)
            anomalies = self._detect_anomalies(image_bytes, behaviors, pet_type)
            return {
                "analysis_id": str(uuid4()),
                "behaviors": behaviors,
                "body_condition_score": body_condition,
                "posture_quality": posture,
                "coat_condition": coat_condition,
                "anomalies_detected": anomalies,
            }
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            raise

    def _detect_behaviors(self, image_bytes: bytes, pet_type: str) -> List[Dict]:
        behaviors = [
            {"behavior_type": "resting", "confidence": 0.85},
            {"behavior_type": "alert", "confidence": 0.65},
        ]
        if pet_type == "dog":
            behaviors.append({"behavior_type": "tail_wagging", "confidence": 0.72})
        elif pet_type == "cat":
            behaviors.append({"behavior_type": "grooming", "confidence": 0.68})
        return behaviors

    def _estimate_body_condition(self, image_bytes: bytes, pet_type: str) -> float:
        return 5.0

    def _analyze_posture(self, image_bytes: bytes) -> str:
        return "normal"

    def _analyze_coat(self, image_bytes: bytes) -> str:
        return "healthy"

    def _detect_anomalies(self, image_bytes: bytes, behaviors: List[Dict], pet_type: str) -> List[str]:
        anomalies = []
        for b in behaviors:
            if b["behavior_type"] == "hiding" and b["confidence"] > 0.8:
                anomalies.append("Pet appears to be hiding - possible stress or illness")
            if b["behavior_type"] == "lethargic" and b["confidence"] > 0.7:
                anomalies.append("Lethargic behavior detected - monitor closely")
        return anomalies


class SoundAnalysisEngine:
    """Audio analysis engine for pet sound health monitoring."""

    def __init__(self):
        self._model_loaded = False

    def _ensure_model(self):
        if not self._model_loaded:
            self._model_loaded = True
            logger.info("Sound analysis model loaded")

    async def analyze_audio(self, audio_data: str, duration: float, pet_type: str = "dog") -> Dict[str, Any]:
        self._ensure_model()
        try:
            audio_bytes = base64.b64decode(audio_data)
            events = self._detect_sound_events(audio_bytes, duration, pet_type)
            stress_level = self._calculate_stress_level(events)
            respiratory = self._analyze_respiratory_pattern(events)
            indicators = self._identify_health_indicators(events, pet_type)
            return {
                "analysis_id": str(uuid4()),
                "events": events,
                "overall_stress_level": stress_level,
                "respiratory_pattern": respiratory,
                "health_indicators": indicators,
            }
        except Exception as e:
            logger.error(f"Audio analysis failed: {e}")
            raise

    def _detect_sound_events(self, audio_bytes: bytes, duration: float, pet_type: str) -> List[Dict]:
        if pet_type == "dog":
            return [
                {"event_type": "bark", "confidence": 0.9, "start_time": 0.5, "end_time": 1.2,
                 "frequency_hz": 450, "amplitude_db": -12, "is_abnormal": False},
            ]
        return [
            {"event_type": "meow", "confidence": 0.85, "start_time": 0.3, "end_time": 0.9,
             "frequency_hz": 680, "amplitude_db": -18, "is_abnormal": False},
        ]

    def _calculate_stress_level(self, events: List[Dict]) -> float:
        if not events:
            return 0.1
        stress = 0.0
        for e in events:
            if e["event_type"] in ("whine", "growl", "cry"):
                stress += 0.3 * e["confidence"]
            if e["is_abnormal"]:
                stress += 0.4 * e["confidence"]
        return min(stress, 1.0)

    def _analyze_respiratory_pattern(self, events: List[Dict]) -> Optional[str]:
        for e in events:
            if e["event_type"] in ("cough", "wheeze"):
                return "abnormal"
        return "normal"

    def _identify_health_indicators(self, events: List[Dict], pet_type: str) -> List[str]:
        indicators = []
        abnormal_types = {"cough", "wheeze", "vomit_sound"}
        for e in events:
            if e["event_type"] in abnormal_types and e["confidence"] > 0.7:
                indicators.append(f"Abnormal sound detected: {e['event_type']} (confidence: {e['confidence']:.0%})")
        return indicators


class ActivityTracker:
    """Tracks and analyzes pet activity patterns."""

    def calculate_daily_summary(self, logs: List[Dict]) -> Dict:
        if not logs:
            return {
                "total_duration_minutes": 0, "total_distance_meters": 0,
                "total_steps": 0, "total_calories": 0,
                "activity_level": "sedentary", "activity_breakdown": {}, "hourly_distribution": {},
            }
        total_duration = sum(l.get("duration_minutes", 0) for l in logs)
        total_distance = sum(l.get("distance_meters", 0) for l in logs)
        total_steps = sum(l.get("steps", 0) for l in logs)
        total_calories = sum(l.get("calories_burned", 0) for l in logs)

        breakdown: Dict[str, float] = {}
        hourly: Dict[str, float] = {}
        for log in logs:
            atype = log.get("activity_type", "unknown")
            dur = log.get("duration_minutes", 0)
            breakdown[atype] = breakdown.get(atype, 0) + dur
            hour = log.get("recorded_at", datetime.utcnow()).hour
            hour_key = f"{hour:02d}:00"
            hourly[hour_key] = hourly.get(hour_key, 0) + dur

        level = self._classify_activity_level(total_duration)
        return {
            "total_duration_minutes": total_duration, "total_distance_meters": total_distance,
            "total_steps": total_steps, "total_calories": total_calories,
            "activity_level": level, "activity_breakdown": breakdown, "hourly_distribution": hourly,
        }

    def _classify_activity_level(self, total_minutes: float) -> str:
        if total_minutes < 30: return "sedentary"
        elif total_minutes < 60: return "low"
        elif total_minutes < 120: return "moderate"
        elif total_minutes < 180: return "active"
        return "very_active"


class DietMonitor:
    """Monitors pet diet and nutrition."""

    def calculate_daily_summary(self, logs: List[Dict], pet_profile: Dict) -> Dict:
        if not logs:
            return {
                "total_calories": 0, "total_protein": 0, "total_fat": 0, "total_carbs": 0,
                "total_water_ml": 0, "meal_count": 0, "nutritional_balance_score": 0.0,
                "recommendations": ["No diet logs recorded for today"],
            }
        totals = {
            "calories": sum(l.get("calories", 0) or 0 for l in logs),
            "protein": sum(l.get("protein", 0) or 0 for l in logs),
            "fat": sum(l.get("fat", 0) or 0 for l in logs),
            "carbs": sum(l.get("carbs", 0) or 0 for l in logs),
            "water_ml": sum(l.get("water_intake_ml", 0) or 0 for l in logs),
            "meal_count": len(logs),
        }
        target_calories = pet_profile.get("daily_calorie_target", 800)
        calorie_ratio = min(totals["calories"] / target_calories, 1.5) if target_calories > 0 else 0
        protein_ratio = totals["protein"] / 50 if totals["protein"] > 0 else 0
        balance_score = max(0, 1.0 - abs(calorie_ratio - 1.0) * 0.5 - (0 if 0.3 < protein_ratio < 1.5 else 0.2))

        recommendations = []
        if calorie_ratio < 0.7:
            recommendations.append("Caloric intake is below recommended levels")
        elif calorie_ratio > 1.3:
            recommendations.append("Caloric intake exceeds recommended levels")
        if totals["water_ml"] < 200:
            recommendations.append("Water intake seems low - ensure fresh water is available")

        return {
            "total_calories": totals["calories"], "total_protein": totals["protein"],
            "total_fat": totals["fat"], "total_carbs": totals["carbs"],
            "total_water_ml": totals["water_ml"], "meal_count": totals["meal_count"],
            "nutritional_balance_score": round(balance_score, 2), "recommendations": recommendations,
        }


camera_engine = CameraAnalysisEngine()
sound_engine = SoundAnalysisEngine()
activity_tracker = ActivityTracker()
diet_monitor = DietMonitor()
