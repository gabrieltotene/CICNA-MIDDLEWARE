"""Adaptador WhatsApp - Implementação para WhatsApp Business API."""
from typing import Optional, Dict, Any
from datetime import datetime
import httpx

from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter
from src.domain.entities.message import Message, MessageType, MessageStatus


class EvolutionWhatsAppAdapter(IMessagingPlatformAdapter):
    """
    Adaptador para WhatsApp Business API.
    
    Implementa a interface IMessagingPlatformAdapter para comunicação
    com a API do WhatsApp Business.
    """

    def __init__(self, api_key: str, evolution_url: str, instance: str):
        """
        Inicializa o adaptador WhatsApp.
        
        Args:
            api_token: Token de acesso da API do WhatsApp
            phone_number_id: ID do número de telefone do WhatsApp Business
            api_url: URL base da API (padrão: Graph API v18.0)
        """
        self.evolution_url = evolution_url
        self.api_key = api_key
        self.instance = instance
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
    
    async def send_message(self, message: Message) -> bool:
        """Envia uma mensagem através do WhatsApp."""
        try:
            if message.message_type == MessageType.TEXT:
                return await self.send_text(message.recipient_id, message.content)
            elif message.message_type == MessageType.INTERACTIVE:
                # Implementar mensagens interativas
                return await self.send_interactive_message(message.recipient_id, message.content, [])
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
            if webhook_data.get("event") != "messages.upsert":
                return None
            
            data = webhook_data.get("data", {})
            key = data.get("key", {})

            remote_jid = key.get("remoteJid")
            message_content = data.get("message", {})

            button_response = message_content.get("buttonResponseMessage")
            if button_response:
                content = button_response.get('selectedButtonId')
            else:
                content = (message_content.get("conversation") or
                        message_content.get("extendedTextMessage", {}).get("text"))
            
            if not content:
                return None
            
            timestamp_str = data.get("messageTimestamp")
            timestamp = datetime.fromtimestamp(int(timestamp_str) if timestamp_str else datetime.now().timestamp())

            message_id = key.get("id", f"evo_{timestamp}")

            return Message(
                id = message_id,
                sender_id=remote_jid,
                recipient_id="system",
                content=content,
                message_type=MessageType.TEXT,
                platform="whatsapp",
                timestamp=timestamp,
                status=MessageStatus.DELIVERED,
                metadata=data
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

            url = f"{self.evolution_url}/message/sendText/{self.instance}"
            
            payload = {
                "number": recipient_id,
                "options" : {"delay": 1200, "preview_url": True},
                "text" : text
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
            print(f"Enviando mensagem interativa para {recipient_id} com texto: {text} e botões: {buttons}")

            clean_number = recipient_id.replace("@s.whatsapp.net", "").replace("@c.us", "")
            url = f"{self.evolution_url}/message/sendList/{self.instance}"
            print(f"URL de envio: {url}")

            formatted_buttons = []
            for btn in buttons[:3]:
                formatted_buttons.append({
                    "title": btn["reply"]["title"],
                    "rowId": btn["reply"]["id"],
                    "description" : btn["reply"]["title"]
                })

            print(f"Botões formatados: {formatted_buttons}")

            payload = {
                "number": recipient_id,
                "title": "Menu de Opções",
                "description" : text,
                "buttonText" : "Selecione uma opção",
                "footerText":"Powered by CICNA",
                "sections": [
                    {
                        "title": "Opções disponíveis",
                        "rows": formatted_buttons
                    }
                ]
            }

            print(f"Payload de envio: {payload}")

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30.0)
                
                print(f"\n=== RESPOSTA DA API ===")
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")
                print(f"Response Headers: {dict(response.headers)}")
                
                success = response.status_code in [200, 201]
                print(f"Considerado sucesso: {success}")
                return success
        except Exception as e:
            print(f"Erro ao enviar mensagem interativa: {e}")
            return await self.send_text(recipient_id, text)

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
        return "event" in request_data and "data" in request_data
