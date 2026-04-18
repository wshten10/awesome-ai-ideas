"""
AI SafetyMate - Industrial Safety AI System
==========================================

An industrial safety AI system designed for blue-collar workers and safety officers,
providing real-time monitoring, multilingual support, and predictive maintenance guidance.
"""

__version__ = "1.0.0"
__author__ = "wshten10"
__email__ = "ten.ex@example.com"

from .core.monitoring import SafetyMonitor
from .core.voice_assistant import VoiceAssistant
from .core.ar_assistance import ARAssistant
from .core.maintenance import PredictiveMaintenance
from .core.knowledge_base import KnowledgeBase

__all__ = [
    'SafetyMonitor',
    'VoiceAssistant', 
    'ARAssistant',
    'PredictiveMaintenance',
    'KnowledgeBase'
]