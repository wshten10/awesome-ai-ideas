"""
Knowledge Graph - REST API endpoints.
"""
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException
from backend.knowledge_graph.models import (
    SymptomCheckRequest, SymptomCheckResponse, NutritionQueryRequest, NutritionQueryResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse, DiseaseDetailRequest, DiseaseDetail,
    DiseaseMatch, NutrientRecommendation, FoodSuggestion, KnowledgeArticle,
)
from backend.knowledge_graph.engine import symptom_checker, nutrition_engine, knowledge_search, DISEASE_DATABASE

router = APIRouter()


@router.post("/symptom-check", response_model=SymptomCheckResponse)
async def check_symptoms(request: SymptomCheckRequest):
    """AI-powered symptom analysis and disease matching."""
    matches, summary = symptom_checker.analyze_symptoms(
        symptoms=request.symptoms, pet_type=request.pet_type, breed=request.breed,
        age_years=request.age_years, duration_days=request.duration_days, severity=request.severity,
    )
    return SymptomCheckResponse(
        pet_id=request.pet_id, check_id=f"sc-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        timestamp=datetime.utcnow(), reported_symptoms=request.symptoms,
        possible_diseases=[DiseaseMatch(**m) for m in matches], summary=summary,
    )


@router.post("/nutrition/query", response_model=NutritionQueryResponse)
async def query_nutrition(request: NutritionQueryRequest):
    """Get personalized nutrition recommendations."""
    result = nutrition_engine.get_recommendations(
        pet_type=request.pet_type, breed=request.breed, age_years=request.age_years,
        weight_kg=request.weight_kg, activity_level=request.activity_level,
        health_conditions=request.health_conditions, life_stage=request.life_stage,
    )
    return NutritionQueryResponse(
        pet_profile=result["pet_profile"], daily_calorie_target=result["daily_calorie_target"],
        nutrient_recommendations=[NutrientRecommendation(**n) for n in result["nutrient_recommendations"]],
        food_suggestions=[FoodSuggestion(**f) for f in result["food_suggestions"]],
        foods_to_avoid=result["foods_to_avoid"], feeding_schedule=result["feeding_schedule"],
        special_notes=result["special_notes"],
    )


@router.post("/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(request: KnowledgeSearchRequest):
    """Search the veterinary knowledge base."""
    results, suggestions = knowledge_search.search(
        query=request.query, pet_type=request.pet_type, category=request.category, limit=request.limit,
    )
    return KnowledgeSearchResponse(query=request.query, results=[KnowledgeArticle(**a) for a in results],
                                    total_count=len(results), suggestions=suggestions)


@router.post("/disease/detail", response_model=DiseaseDetail)
async def get_disease_detail(request: DiseaseDetailRequest):
    """Get detailed information about a specific disease."""
    diseases = DISEASE_DATABASE.get(request.pet_type, [])
    for d in diseases:
        if d["name"].lower() == request.disease_name.lower():
            return DiseaseDetail(
                name=d["name"], pet_types=[request.pet_type], description=d["description"],
                causes=["Various environmental and genetic factors"], symptoms=d["common_symptoms"],
                diagnosis_methods=["Physical examination", "Blood tests", "Imaging"],
                treatment_options=d["actions"], prevention=["Regular checkups", "Vaccination", "Proper nutrition"],
                prognosis="Varies by severity", when_to_see_vet=d["actions"][0] if d["actions"] else "Consult vet",
                related_diseases=[], references=["Veterinary Internal Medicine Textbook"],
            )
    raise HTTPException(status_code=404, detail="Disease not found")
