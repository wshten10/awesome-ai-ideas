"""
Community - Pydantic models.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserMatchRequest(BaseModel):
    user_id: UUID
    pet_type: Optional[str] = None
    breed: Optional[str] = None
    location_radius_km: Optional[int] = Field(default=50)
    interests: List[str] = Field(default_factory=list)
    limit: int = Field(default=10, ge=1, le=50)


class UserMatch(BaseModel):
    user_id: UUID
    username: str
    avatar_url: Optional[str]
    location: Optional[str]
    pets: List[Dict[str, str]]
    match_score: float = Field(ge=0.0, le=1.0)
    match_reasons: List[str]


class UserMatchResponse(BaseModel):
    matches: List[UserMatch]
    total_count: int


class PostCreateRequest(BaseModel):
    author_id: UUID
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    post_type: str = Field(default="experience")  # experience, question, tip, review
    tags: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)


class PostResponse(BaseModel):
    id: str
    author_username: str
    author_avatar: Optional[str]
    title: str
    content: str
    post_type: str
    tags: List[str]
    images: List[str]
    likes_count: int
    comments_count: int
    created_at: datetime


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total_count: int
    has_more: bool


class QAQuestionCreate(BaseModel):
    author_id: UUID
    pet_id: Optional[UUID] = None
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    tags: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)


class QAAnswerCreate(BaseModel):
    question_id: UUID
    author_id: UUID
    content: str = Field(..., min_length=5)
    is_expert: bool = False


class QAQuestionResponse(BaseModel):
    id: str
    author_username: str
    title: str
    content: str
    tags: List[str]
    images: List[str]
    is_resolved: bool
    expert_answered: bool
    views_count: int
    answers_count: int
    created_at: datetime
    answers: List[Dict[str, Any]] = Field(default_factory=list)


class QAQuestionListResponse(BaseModel):
    questions: List[QAQuestionResponse]
    total_count: int
    has_more: bool
