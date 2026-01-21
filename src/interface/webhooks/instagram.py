"""Webhook para Instagram."""
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/instagram")
async def instagram_webhook(request: Request):
    """
    Endpoint para receber mensagens do Instagram.
    
    Processa webhooks enviados pelo Instagram Messaging API.
    """
    # Implementação futura
    return {"success": True, "message": "Instagram webhook - em desenvolvimento"}
