"""Entidade Conversation - Representa uma conversa no sistema."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class ConversationStatus(Enum):
    """Status da conversa."""
    ACTIVE = "active"
    CLOSED = "closed"
    WAITING = "waiting"


@dataclass
class Conversation:
    """
    Entidade Conversation.
    
    Representa uma conversa entre um usuário e o sistema,
    gerenciada através do Typebot.
    """
    id: str
    user_id: str
    platform: str
    typebot_session_id: Optional[str] = None
    status: ConversationStatus = ConversationStatus.ACTIVE
    started_at: datetime = field(default_factory=datetime.now)
    last_interaction: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None
    message_ids: List[str] = field(default_factory=list)
    
    def add_message(self, message_id: str) -> None:
        """Adiciona uma mensagem à conversa."""
        self.message_ids.append(message_id)
        self.last_interaction = datetime.now()
    
    def close(self) -> None:
        """Fecha a conversa."""
        self.status = ConversationStatus.CLOSED
