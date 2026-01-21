"""Entidade Message - Representa uma mensagem no sistema."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class MessageType(Enum):
    """Tipos de mensagem suportados."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    INTERACTIVE = "interactive"


class MessageStatus(Enum):
    """Status de entrega da mensagem."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


@dataclass
class Message:
    """
    Entidade Message.
    
    Representa uma mensagem genérica que pode ser enviada/recebida
    através de diferentes plataformas (WhatsApp, Instagram, Twitter, etc).
    """
    id: str
    sender_id: str
    recipient_id: str
    content: str
    message_type: MessageType
    platform: str
    timestamp: datetime
    status: MessageStatus = MessageStatus.PENDING
    metadata: Optional[Dict[str, Any]] = None
    reply_to: Optional[str] = None
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if not self.sender_id:
            raise ValueError("sender_id não pode ser vazio")
        if not self.recipient_id:
            raise ValueError("recipient_id não pode ser vazio")
        if not self.content and self.message_type == MessageType.TEXT:
            raise ValueError("content não pode ser vazio para mensagens de texto")
