"""
Safety Monitor - Computer Vision Module
======================================

Real-time workplace hazard detection and PPE compliance monitoring using computer vision.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from ultralytics import YOLO
import logging
from dataclasses import dataclass
from enum import Enum

class HazardType(Enum):
    """Types of workplace hazards that can be detected"""
    NO_PPE_HELMET = "no_ppe_helmet"
    NO_PPE_VEST = "no_ppe_vest" 
    NO_PPE_GLOVES = "no_ppe_gloves"
    UNSAFE_LIFTING = "unsafe_lifting"
    SLIP_TRIP_HAZARD = "slip_trip_hazard"
    FIRE_HAZARD = "fire_hazard"
    CHEMICAL_SPILL = "chemical_spill"
    ELECTRICAL_HAZARD = "electrical_hazard"
    MACHINERY_GUARD_MISSING = "machinery_guard_missing"
    UNSAFE_POSTURE = "unsafe_posture"

@dataclass
class DetectionResult:
    """Result of a hazard detection"""
    hazard_type: HazardType
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    timestamp: float
    location: Optional[str] = None
    severity: str = "medium"  # low, medium, high

class SafetyMonitor:
    """
    Real-time safety monitoring system using computer vision.
    
    Features:
    - PPE compliance detection
    - Workplace hazard identification  
    - Unsafe behavior detection
    - Real-time alerts and notifications
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the safety monitor.
        
        Args:
            model_path: Path to custom YOLO model (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.model = self._load_model(model_path)
        self.detection_history = []
        self.alert_threshold = 0.7  # Minimum confidence for alert
        
    def _load_model(self, model_path: str = None) -> YOLO:
        """Load YOLO model for hazard detection"""
        try:
            if model_path and model_path.exists():
                return YOLO(str(model_path))
            else:
                # Load pre-trained model for industrial safety
                return YOLO('yolov8n.pt')  # Will be fine-tuned for industrial use
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def detect_hazards(self, frame: np.ndarray) -> List[DetectionResult]:
        """
        Detect workplace hazards in a video frame.
        
        Args:
            frame: Video frame as numpy array
            
        Returns:
            List of detected hazards
        """
        try:
            # Run inference
            results = self.model(frame)
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extract detection info
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        # Convert to our hazard types (mapping needed)
                        hazard_type = self._map_detection_to_hazard(class_id)
                        
                        if confidence >= self.alert_threshold:
                            detection = DetectionResult(
                                hazard_type=hazard_type,
                                confidence=confidence,
                                bbox=(x1, y1, x2, y2),
                                timestamp=cv2.getTickCount() / cv2.getTickFrequency()
                            )
                            detections.append(detection)
            
            self.detection_history.extend(detections)
            return detections
            
        except Exception as e:
            self.logger.error(f"Hazard detection failed: {e}")
            return []
    
    def _map_detection_to_hazard(self, class_id: int) -> HazardType:
        """Map YOLO class IDs to our hazard types"""
        # This is a simplified mapping - in production would use custom trained model
        hazard_mapping = {
            0: HazardType.NO_PPE_HELMET,
            1: HazardType.NO_PPE_VEST,
            2: HazardType.NO_PPE_GLOVES,
            # ... add more mappings based on custom training
        }
        return hazard_mapping.get(class_id, HazardType.UNSAFE_POSTURE)
    
    def detect_ppe_compliance(self, frame: np.ndarray) -> Dict[str, bool]:
        """
        Detect PPE compliance for workers in the frame.
        
        Args:
            frame: Video frame as numpy array
            
        Returns:
            Dictionary indicating PPE compliance status
        """
        ppe_status = {
            "helmet": False,
            "vest": False, 
            "gloves": False,
            "glasses": False
        }
        
        # Detect PPE (simplified - would use specialized models)
        detections = self.detect_hazards(frame)
        
        for detection in detections:
            if detection.hazard_type == HazardType.NO_PPE_HELMET:
                ppe_status["helmet"] = True  # Inverted: detected = compliance
            elif detection.hazard_type == HazardType.NO_PPE_VEST:
                ppe_status["vest"] = True
            elif detection.hazard_type == HazardType.NO_PPE_GLOVES:
                ppe_status["gloves"] = True
                
        return ppe_status
    
    def calculate_safety_score(self, frame: np.ndarray) -> float:
        """
        Calculate overall safety score for the workspace.
        
        Args:
            frame: Video frame as numpy array
            
        Returns:
            Safety score from 0-100
        """
        detections = self.detect_hazards(frame)
        ppe_status = self.detect_ppe_compliance(frame)
        
        # Calculate score based on violations
        violations = len(detections)
        ppe_violations = sum(1 for compliant in ppe_status.values() if not compliant)
        
        # Simple scoring algorithm
        base_score = 100
        violation_penalty = violations * 5
        ppe_penalty = ppe_violations * 3
        
        safety_score = max(0, base_score - violation_penalty - ppe_penalty)
        return safety_score
    
    def get_recent_alerts(self, time_window: float = 300) -> List[DetectionResult]:
        """
        Get recent alerts within a time window (seconds).
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            List of recent alerts
        """
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        cutoff_time = current_time - time_window
        
        recent_alerts = [
            alert for alert in self.detection_history 
            if alert.timestamp >= cutoff_time
        ]
        
        return recent_alerts
    
    def start_real_time_monitoring(self, camera_source: int = 0):
        """
        Start real-time monitoring from camera feed.
        
        Args:
            camera_source: Camera index or video file path
        """
        cap = cv2.VideoCapture(camera_source)
        
        if not cap.isOpened():
            self.logger.error("Failed to open camera source")
            return
        
        self.logger.info("Starting real-time safety monitoring...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect hazards
            detections = self.detect_hazards(frame)
            ppe_status = self.detect_ppe_compliance(frame)
            safety_score = self.calculate_safety_score(frame)
            
            # Display results (for demo)
            self._display_results(frame, detections, ppe_status, safety_score)
            
            # Check for critical alerts
            critical_alerts = [d for d in detections if d.severity == "high"]
            if critical_alerts:
                self.logger.warning(f"Critical alert detected: {len(critical_alerts)} hazards")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def _display_results(self, frame: np.ndarray, detections: List[DetectionResult], 
                       ppe_status: Dict[str, bool], safety_score: float):
        """Display detection results on frame (for demo)"""
        # Draw bounding boxes
        for detection in detections:
            x1, y1, x2, y2 = detection.bbox
            color = (0, 0, 255) if detection.severity == "high" else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, detection.hazard_type.value, (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Display safety score
        cv2.putText(frame, f"Safety Score: {safety_score:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Display PPE status
        ppe_text = "PPE: " + ", ".join([f"{k}: {'✓' if v else '✗'}" 
                                     for k, v in ppe_status.items()])
        cv2.putText(frame, ppe_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('AI SafetyMate - Safety Monitoring', frame)