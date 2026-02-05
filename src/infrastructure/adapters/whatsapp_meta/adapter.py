from typing import Optional, Dict, Any
from datetime import datetime
import httpx

from src.domain.entities.message import Message, MessageType, MessageStatus
from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter


class WhatsAppMetaAdapter(IMessagingPlatformAdapter):
    """
    Adaptador para WhatsApp business API.

    Implementa a interface IMessagingPlatformAdapter  para comuinicação
    com a API do WhatsApp Business.
    """

    