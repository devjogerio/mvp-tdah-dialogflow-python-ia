from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class User:
    user_id: str
    created_at: datetime
    preferences: Optional[dict] = None


@dataclass
class Message:
    content: str
    role: str  # 'user' | 'assistant' | 'system'
    created_at: datetime


@dataclass
class Session:
    session_id: str
    user_id: str
    messages: List[Message]
    context: Optional[dict] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
