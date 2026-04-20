"""
Training Assistant - Core training engine.
"""
import logging
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

BREED_PROFILES: Dict[str, Dict] = {
    "labrador": {"trainability": "high", "attention_span": "medium", "energy_level": "high",
                 "food_motivation": "very_high", "play_motivation": "high",
                 "recommended_skills": ["sit", "stay", "come", "heel", "retrieve", "leave_it"]},
    "golden_retriever": {"trainability": "high", "attention_span": "medium", "energy_level": "medium",
                         "food_motivation": "high", "play_motivation": "high",
                         "recommended_skills": ["sit", "stay", "come", "shake", "roll_over"]},
    "german_shepherd": {"trainability": "high", "attention_span": "long", "energy_level": "high",
                        "food_motivation": "medium", "play_motivation": "very_high",
                        "recommended_skills": ["sit", "stay", "come", "heel", "place", "speak"]},
    "poodle": {"trainability": "very_high", "attention_span": "long", "energy_level": "medium",
               "food_motivation": "medium", "play_motivation": "high",
               "recommended_skills": ["sit", "stay", "come", "shake", "spin", "fetch"]},
    "bulldog": {"trainability": "medium", "attention_span": "short", "energy_level": "low",
                "food_motivation": "very_high", "play_motivation": "low",
                "recommended_skills": ["sit", "stay", "come", "leave_it"]},
    "persian_cat": {"trainability": "low", "attention_span": "short", "energy_level": "low",
                    "food_motivation": "high", "play_motivation": "low",
                    "recommended_skills": ["come", "sit", "high_five"]},
    "siamese_cat": {"trainability": "medium", "attention_span": "medium", "energy_level": "high",
                    "food_motivation": "medium", "play_motivation": "very_high",
                    "recommended_skills": ["come", "sit", "high_five", "fetch", "spin"]},
}

SKILL_DEFINITIONS: Dict[str, Dict] = {
    "sit": {
        "difficulty": "beginner", "estimated_minutes": 10, "prerequisites": [], "equipment": ["treats", "clicker (optional)"],
        "steps": [
            {"action": "Get Attention", "duration": 15, "description": "Stand in front of your pet with a treat.",
             "tips": ["Choose a quiet environment", "Wait for eye contact"], "success_criteria": "Pet is focused on you"},
            {"action": "Lure Over Head", "duration": 20, "description": "Move the treat from nose up and back over head.",
             "tips": ["Move slowly", "Keep treat close to nose"], "success_criteria": "Pet's bottom touches the ground"},
            {"action": "Mark and Reward", "duration": 10, "description": "Say 'Yes!' or click when bottom touches ground, give treat.",
             "tips": ["Timing is crucial", "Reward immediately"], "success_criteria": "Clear marker-reward sequence"},
            {"action": "Add Cue", "duration": 15, "description": "Say 'Sit' before luring. Gradually reduce hand lure.",
             "tips": ["Say cue only once", "Be patient"], "success_criteria": "Pet responds to verbal cue"},
            {"action": "Repeat and Practice", "duration": 30, "description": "Repeat 5-10 times in short sessions.",
             "tips": ["Keep sessions short", "End on success"], "success_criteria": "Pet sits on cue 8/10 times"},
        ],
    },
    "stay": {
        "difficulty": "beginner", "estimated_minutes": 15, "prerequisites": ["sit"], "equipment": ["treats"],
        "steps": [
            {"action": "Position and Cue", "duration": 10, "description": "Ask pet to sit, stand in front.",
             "tips": ["Start in quiet area"], "success_criteria": "Pet sitting calmly"},
            {"action": "Hand Signal and Step Back", "duration": 15, "description": "Show palm, say 'Stay', step back, return, reward.",
             "tips": ["One step initially"], "success_criteria": "Pet maintains sit for 1 step"},
            {"action": "Increase Distance", "duration": 30, "description": "Gradually increase to 2, 3, 5 steps.",
             "tips": ["Return and reward each success"], "success_criteria": "Pet stays for 5 steps"},
            {"action": "Add Duration", "duration": 30, "description": "Build to 5, 10, 15 seconds of stay.",
             "tips": ["Release with 'Okay!'"], "success_criteria": "Pet stays for 15 seconds at 5 steps"},
        ],
    },
    "come": {
        "difficulty": "beginner", "estimated_minutes": 15, "prerequisites": [], "equipment": ["treats", "long line"],
        "steps": [
            {"action": "Crouch and Call", "duration": 15, "description": "Crouch down, open arms, call excitedly.",
             "tips": ["High-value treats", "Never call for punishment"], "success_criteria": "Pet moves toward you"},
            {"action": "Reward Enthusiastically", "duration": 10, "description": "Give lots of praise and treats when pet reaches you.",
             "tips": ["Jackpot rewards"], "success_criteria": "Pet comes quickly"},
            {"action": "Practice with Distance", "duration": 30, "description": "Use long line at increasing distances.",
             "tips": ["Start at 3m, build to 10m+"], "success_criteria": "Pet comes reliably from 10m"},
        ],
    },
}


class TrainingPlanGenerator:
    """Generates personalized training plans."""

    def generate_plan(self, goals: List[str], breed: Optional[str] = None,
                      current_level: str = "beginner", daily_time_budget: int = 15,
                      preferred_style: str = "positive_reinforcement") -> Dict:
        profile = BREED_PROFILES.get(breed, {"trainability": "medium", "attention_span": "medium",
                                              "energy_level": "medium", "food_motivation": "high",
                                              "play_motivation": "medium", "recommended_skills": ["sit", "stay", "come"]})
        selected_skills = self._select_skills(goals, profile)
        weekly_schedule = self._create_schedule(selected_skills, daily_time_budget)
        milestones = self._define_milestones(selected_skills)
        return {
            "plan_id": str(uuid4()), "created_at": datetime.utcnow(), "goals": goals,
            "weekly_schedule": weekly_schedule, "milestones": milestones,
            "estimated_completion_weeks": len(selected_skills),
            "tips": self._generate_tips(profile, preferred_style),
        }

    def _select_skills(self, goals: List[str], profile: Dict) -> List[Dict]:
        goal_map = {"basic_obedience": ["sit", "stay", "come"], "leash_training": ["sit", "stay", "heel"],
                    "tricks": ["shake", "spin", "roll_over"], "manners": ["sit", "stay", "leave_it"]}
        skills = []
        seen = set()
        for goal in goals:
            for name in goal_map.get(goal, ["sit", "stay"]):
                if name not in seen and name in SKILL_DEFINITIONS:
                    seen.add(name)
                    skills.append({"name": name, **SKILL_DEFINITIONS[name]})
        for name in profile.get("recommended_skills", []):
            if name not in seen and name in SKILL_DEFINITIONS:
                seen.add(name)
                skills.append({"name": name, **SKILL_DEFINITIONS[name]})
        return skills[:7]  # Limit to manageable number

    def _create_schedule(self, skills: List[Dict], budget: int) -> List[Dict]:
        schedule = []
        for i, skill in enumerate(skills):
            schedule.append({
                "session_id": f"session-{i+1}-{skill['name']}",
                "skill_name": skill["name"],
                "difficulty": skill["difficulty"],
                "estimated_duration_minutes": min(skill["estimated_minutes"], budget),
                "steps": [{"step_number": j+1, **step} for j, step in enumerate(skill["steps"])],
                "equipment_needed": skill["equipment"],
                "prerequisites": skill["prerequisites"],
            })
        return schedule

    def _define_milestones(self, skills: List[Dict]) -> List[Dict]:
        milestones = []
        for i, skill in enumerate(skills):
            milestones.append({"week": i+1, "skill": skill["name"],
                              "target": f"Master {skill['name']} with 80%+ success rate",
                              "celebration": f"Great progress on {skill['name']}!"})
        return milestones

    def _generate_tips(self, profile: Dict, style: str) -> List[str]:
        tips = [f"Your pet's trainability is rated '{profile.get('trainability', 'medium')}'",
                f"Attention span is '{profile.get('attention_span', 'medium')}' - keep sessions short"]
        if profile.get("food_motivation") in ("high", "very_high"):
            tips.append("Use food treats as primary motivation")
        if profile.get("play_motivation") in ("high", "very_high"):
            tips.append("Incorporate play into training sessions")
        return tips


class ProgressTracker:
    """Tracks training progress and provides feedback."""

    def log_session(self, skill_name: str, success_rating: float, duration_minutes: int,
                    notes: Optional[str] = None) -> Dict:
        feedback = self._generate_feedback(skill_name, success_rating, duration_minutes)
        next_steps = self._suggest_next_steps(skill_name, success_rating)
        return {"log_id": str(uuid4()), "feedback": feedback, "next_steps": next_steps}

    def _generate_feedback(self, skill: str, rating: float, duration: int) -> str:
        if rating >= 0.8:
            return f"Excellent work on {skill}! {rating:.0%} success rate in {duration} minutes. Your pet is learning fast!"
        elif rating >= 0.5:
            return f"Good progress on {skill} with {rating:.0%} success rate. Keep practicing with shorter sessions."
        else:
            return f"{skill} needs more practice ({rating:.0%}). Try breaking it into smaller steps and using higher-value rewards."

    def _suggest_next_steps(self, skill: str, rating: float) -> List[str]:
        if rating >= 0.8:
            return [f"Add distractions to {skill} practice", f"Practice {skill} in new locations",
                    f"Move to the next skill in your plan"]
        elif rating >= 0.5:
            return [f"Continue practicing {skill}", "Try increasing duration between rewards",
                    "Practice in slightly more distracting environments"]
        return [f"Go back to basics with {skill}", "Use higher-value treats",
                "Keep sessions very short (3-5 minutes)", "Ensure pet is not tired or distracted"]


class RealTimeGuidanceEngine:
    """Provides real-time training guidance."""

    def analyze_step(self, skill: str, step: int, description: Optional[str] = None) -> Dict:
        skill_def = SKILL_DEFINITIONS.get(skill, {})
        steps = skill_def.get("steps", [])
        if not steps or step < 1 or step > len(steps):
            return {"feedback": [], "overall_session_rating": 0.5, "session_summary": "Step not found in skill definition"}

        current = steps[step - 1]
        feedback = [{
            "step_number": step, "is_correct": True, "confidence": 0.8,
            "feedback_text": f"Working on: {current['action']}",
            "correction_hint": None,
            "encouragement": "You're doing great! Keep going!",
            "suggested_next_action": current["success_criteria"],
        }]

        return {
            "feedback": feedback,
            "overall_session_rating": 0.75,
            "session_summary": f"Practicing '{current['action']}' for {skill}. Goal: {current['success_criteria']}",
        }


plan_generator = TrainingPlanGenerator()
progress_tracker = ProgressTracker()
guidance_engine = RealTimeGuidanceEngine()
