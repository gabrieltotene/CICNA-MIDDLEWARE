"""Adaptador WhatsApp - Implementação para WhatsApp Business API."""
from typing import Optional, Dict, Any
from datetime import datetime
import httpx

from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter
from src.domain.entities.message import Message, MessageType, MessageStatus


class WhatsAppAdapter(IMessagingPlatformAdapter):
    """
    Adaptador para WhatsApp Business API.
    
    Implementa a interface IMessagingPlatformAdapter para comunicação
    com a API do WhatsApp Business.
    """
    
    def __init__(self, api_token: str, phone_number_id: str, api_url: str = "https://graph.facebook.com/v18.0"):
        """
        Inicializa o adaptador WhatsApp.
        
        Args:
            api_token: Token de acesso da API do WhatsApp
            phone_number_id: ID do número de telefone do WhatsApp Business
            api_url: URL base da API (padrão: Graph API v18.0)
        """
        self.api_token = api_token
        self.phone_number_id = phone_number_id
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def send_message(self, message: Message) -> bool:
        """Envia uma mensagem através do WhatsApp."""
        try:
            if message.message_type == MessageType.TEXT:
                return await self.send_text(message.recipient_id, message.content)
            elif message.message_type == MessageType.INTERACTIVE:
                # Implementar mensagens interativas
                return False
            else:
                # Outros tipos de mídia
                return False
        except Exception:
            return False
    
    async def receive_message(self, webhook_data: Dict[str, Any]) -> Optional[Message]:
        """
        Processa webhook do WhatsApp e converte em Message.
        
        Args:
            webhook_data: Dados do webhook do WhatsApp
            
        Returns:
            Message ou None
        """
        try:
            # Estrutura do webhook do WhatsApp Business API
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
            
            msg_data = messages[0]
            
            # Extrai dados da mensagem
            message_id = msg_data.get("id")
            sender_id = msg_data.get("from")
            timestamp = datetime.fromtimestamp(int(msg_data.get("timestamp", 0)))
            
            # Determina o tipo e conteúdo
            msg_type = msg_data.get("type", "text")
            content = ""
            
            if msg_type == "text":
                content = msg_data.get("text", {}).get("body", "")
                message_type = MessageType.TEXT
            elif msg_type == "image":
                content = msg_data.get("image", {}).get("id", "")
                message_type = MessageType.IMAGE
            else:
                # Outros tipos
                message_type = MessageType.TEXT
                content = f"[{msg_type}]"
            
            return Message(
                id=message_id,
                sender_id=sender_id,
                recipient_id=self.phone_number_id,
                content=content,
                message_type=message_type,
                platform="whatsapp",
                timestamp=timestamp,
                status=MessageStatus.DELIVERED,
                metadata=msg_data
            )
        except Exception:
            return None
    
    async def send_text(self, recipient_id: str, text: str) -> bool:
        """
        Envia mensagem de texto via WhatsApp.
        
        Args:
            recipient_id: Número do destinatário
            text: Texto da mensagem
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            url = f"{self.api_url}/{self.phone_number_id}/messages"
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_id,
                "type": "text",
                "text": {"body": text}
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False
    
    async def send_interactive_message(self, recipient_id: str, text: str, buttons: list) -> bool:
        """
        Envia mensagem interativa com botões.
        
        Args:
            recipient_id: Número do destinatário
            text: Texto da mensagem
            buttons: Lista de botões
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            url = f"{self.api_url}/{self.phone_number_id}/messages"
            
            # Formata botões para o formato do WhatsApp
            formatted_buttons = []
            for idx, button in enumerate(buttons[:3]):  # WhatsApp permite até 3 botões
                formatted_buttons.append({
                    "type": "reply",
                    "reply": {
                        "id": f"btn_{idx}",
                        "title": button[:20]  # Limite de 20 caracteres
                    }
                })
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_id,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": text},
                    "action": {"buttons": formatted_buttons}
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False
    
    def get_platform_name(self) -> str:
        """Retorna o nome da plataforma."""
        return "whatsapp"
    
    async def validate_webhook(self, request_data: Dict[str, Any]) -> bool:
        """
        Valida webhook do WhatsApp.
        
        Args:
            request_data: Dados da requisição
            
        Returns:
            bool: True se válido
        """
        # TODO: Em produção, implementar validação completa
        # Verificar signature do webhook usando app secret
        # https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
        return "entry" in request_data and "object" in request_data
