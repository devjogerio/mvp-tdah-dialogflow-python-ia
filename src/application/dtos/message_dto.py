from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ProcessMessageInput:
    user_id: str
    session_id: str
    message: str
    platform: str  # 'dialogflow' | 'api'
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProcessMessageOutput:
    response_text: str
    risk_detected: bool
    metadata: Optional[Dict[str, Any]] = None
