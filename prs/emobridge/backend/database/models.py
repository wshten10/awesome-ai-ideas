"""
数据库模型定义
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    """患者档案"""
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    diagnosis = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关系
    treatment_sessions = relationship("TreatmentSession", back_populates="patient")
    emotion_records = relationship("EmotionRecord", back_populates="patient")

class Therapist(Base):
    """治疗师档案"""
    __tablename__ = "therapists"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    license_number = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关系
    treatment_sessions = relationship("TreatmentSession", back_populates="therapist")

class TreatmentSession(Base):
    """治疗会话"""
    __tablename__ = "treatment_sessions"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    therapist_id = Column(String, ForeignKey("therapists.id"))
    session_type = Column(String)  # individual, group, family
    session_status = Column(String, default="scheduled")  # scheduled, active, completed, cancelled
    scheduled_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关系
    patient = relationship("Patient", back_populates="treatment_sessions")
    therapist = relationship("Therapist", back_populates="treatment_sessions")
    emotion_records = relationship("EmotionRecord", back_populates="treatment_session")

class EmotionRecord(Base):
    """情感记录"""
    __tablename__ = "emotion_records"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    treatment_session_id = Column(String, ForeignKey("treatment_sessions.id"))
    
    # 情感数据
    emotion_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    intensity = Column(Float, nullable=False)
    
    # 多模态数据
    physiological_data = Column(JSON)  # 生理信号数据
    facial_data = Column(JSON)        # 面部表情数据
    behavioral_data = Column(JSON)     # 行为数据
    voice_data = Column(JSON)         # 语音数据
    bci_data = Column(JSON)           # 脑机接口数据
    
    # 治疗建议
    treatment_recommendation = Column(JSON)
    intervention_intensity = Column(Float)
    expected_outcome = Column(Text)
    
    # 时间戳
    detected_at = Column(DateTime, default=func.now())
    processed_at = Column(DateTime, default=func.now())
    
    # 关系
    patient = relationship("Patient", back_populates="emotion_records")
    treatment_session = relationship("TreatmentSession", back_populates="emotion_records")

class DeviceCalibration(Base):
    """设备校准记录"""
    __tablename__ = "device_calibration"
    
    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # bci, sensor, camera, microphone
    calibration_data = Column(JSON)
    calibration_time = Column(DateTime, default=func.now())
    technician_id = Column(String)

class ModelPerformance(Base):
    """模型性能记录"""
    __tablename__ = "model_performance"
    
    id = Column(String, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    test_scenario = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    test_time = Column(DateTime, default=func.now())

class SystemConfig(Base):
    """系统配置"""
    __tablename__ = "system_config"
    
    id = Column(String, primary_key=True, index=True)
    config_key = Column(String, unique=True, nullable=False)
    config_value = Column(JSON)
    description = Column(Text)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AuditLog(Base):
    """审计日志"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=func.now())

class DigitalTwin(Base):
    """数字孪生数据"""
    __tablename__ = "digital_twin"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    twin_version = Column(String, nullable=False)
    emotional_state = Column(JSON)
    physiological_state = Column(JSON)
    behavioral_patterns = Column(JSON)
    prediction_results = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TherapyEnvironment(Base):
    """治疗环境记录"""
    __tablename__ = "therapy_environment"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("treatment_sessions.id"))
    environment_type = Column(String)  # vr, ar, physical
    environment_config = Column(JSON)
    session_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())