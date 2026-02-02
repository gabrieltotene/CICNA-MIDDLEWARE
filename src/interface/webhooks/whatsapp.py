"""Webhook para WhatsApp."""
from fastapi import APIRouter, Request, Query
from typing import Dict, Any
import httpx

from src.infrastructure.adapters.whatsapp import WhatsAppAdapter
from src.application.services.typebot_service import TypebotService
from src.infrastructure.repositories.in_memory import (
    InMemoryMessageRepository,
    InMemoryUserRepository,
    InMemoryConversationRepository
)
from src.domain.use_cases.process_message import ProcessIncomingMessageUseCase
from src.infrastructure.config.settings import get_settings


router = APIRouter()
settings = get_settings()


def get_whatsapp_use_case() -> ProcessIncomingMessageUseCase:
    """Factory para criar o caso de uso com dependências."""
    adapter = WhatsAppAdapter(
        evolution_url=settings.EVOLUTION_URL,
        api_key=settings.EVOLUTION_API_KEY,
        instance=settings.EVOLUTION_INSTANCE
    )
    
    typebot_service = TypebotService(
        api_url=settings.TYPEBOT_API_URL,
        typebot_id=settings.TYPEBOT_ID,
        api_token=settings.TYPEBOT_API_TOKEN
    )
    
    message_repo = InMemoryMessageRepository()
    user_repo = InMemoryUserRepository()
    conversation_repo = InMemoryConversationRepository()
    
    return ProcessIncomingMessageUseCase(
        messaging_adapter=adapter,
        typebot_service=typebot_service,
        message_repository=message_repo,
        user_repository=user_repo,
        conversation_repository=conversation_repo
    )


@router.get("/whatsapp")
async def whatsapp_webhook_verify():
    """
    Endpoint de verificação do webhook do WhatsApp.
    
    O WhatsApp envia uma requisição GET para verificar o webhook.
    """
    return {"status": "ok"}


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Endpoint para receber mensagens do WhatsApp.
    
    Processa webhooks enviados pelo WhatsApp Business API.
    """
    try:
        # async with httpx.AsyncClient() as client:
        #     body = await client.get("http://localhost:8000/api/mensagens").json()
        #     print(body)

        body = await request.json()
        # Verifica se é uma notificação de mensagem
        if body.get("event") == "messages.upsert":
            use_case = get_whatsapp_use_case()
            result = await use_case.execute(body)
            
            return {"success": True, "result": result}
        
        return {"success": True, "message": "Event processed"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
