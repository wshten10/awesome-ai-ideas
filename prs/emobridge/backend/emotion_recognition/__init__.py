"""
EmoBridge 情感识别模块
多模态情感识别系统
"""

from .engine import EmotionRecognitionEngine
from .models import EmotionState, EmotionDetectionResult
from .processor import MultiModalProcessor

__all__ = [
    "EmotionRecognitionEngine",
    "EmotionState", 
    "EmotionDetectionResult",
    "MultiModalProcessor"
]