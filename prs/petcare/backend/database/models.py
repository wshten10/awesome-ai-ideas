"""
Core database models for PetCare AI.
Defines the base schema for all entities.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime,
    ForeignKey, Enum as SAEnum, JSON, Date
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    pass


class PetType(str, enum.Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    HAMSTER = "hamster"
    FISH = "fish"
    TURTLE = "turtle"
    OTHER = "other"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    location = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    community_posts = relationship("CommunityPost", back_populates="author")
    answers = relationship("QAAnswer", back_populates="author")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    pet_type = Column(SAEnum(PetType), nullable=False)
    breed = Column(String(100), nullable=True)
    gender = Column(SAEnum(Gender), default=Gender.UNKNOWN)
    birth_date = Column(Date, nullable=True)
    weight = Column(Float, nullable=True)
    weight_unit = Column(String(10), default="kg")
    avatar_url = Column(String(500), nullable=True)
    is_neutered = Column(Boolean, default=False)
    microchip_id = Column(String(100), nullable=True)
    allergies = Column(JSON, default=list)
    medical_conditions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="pets")
    health_records = relationship("HealthRecord", back_populates="pet", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="pet", cascade="all, delete-orphan")
    diet_logs = relationship("DietLog", back_populates="pet", cascade="all, delete-orphan")
    training_sessions = relationship("TrainingSession", back_populates="pet", cascade="all, delete-orphan")
    health_alerts = relationship("HealthAlert", back_populates="pet", cascade="all, delete-orphan")


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False, index=True)
    record_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    veterinarian = Column(String(200), nullable=True)
    clinic_name = Column(String(200), nullable=True)
    diagnosis = Column(Text, nullable=True)
    prescription = Column(JSON, default=list)
    attachments = Column(JSON, default=list)
    record_date = Column(DateTime, nullable=False)
    next_visit_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="health_records")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    distance_meters = Column(Float, nullable=True)
    calories_burned = Column(Float, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    recorded_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="activity_logs")


class DietLog(Base):
    __tablename__ = "diet_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False, index=True)
    meal_type = Column(String(50), nullable=False)
    food_name = Column(String(200), nullable=False)
    food_brand = Column(String(200), nullable=True)
    amount_grams = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    water_intake_ml = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    logged_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="diet_logs")


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False, index=True)
    plan_id = Column(UUID(as_uuid=True), nullable=True)
    skill_name = Column(String(200), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    success_rating = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=True)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="training_sessions")


class HealthAlert(Base):
    __tablename__ = "health_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)
    is_dismissed = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    pet = relationship("Pet", back_populates="health_alerts")


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(30), default="experience")
    tags = Column(JSON, default=list)
    images = Column(JSON, default=list)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="community_posts")


class QAQuestion(Base):
    __tablename__ = "qa_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSON, default=list)
    images = Column(JSON, default=list)
    is_resolved = Column(Boolean, default=False)
    expert_answered = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    answers_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    answers = relationship("QAAnswer", back_populates="question", cascade="all, delete-orphan")


class QAAnswer(Base):
    __tablename__ = "qa_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("qa_questions.id"), nullable=False, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_expert = Column(Boolean, default=False)
    likes_count = Column(Integer, default=0)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("QAQuestion", back_populates="answers")
    author = relationship("User", back_populates="answers")
