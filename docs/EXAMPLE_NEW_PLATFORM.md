# Exemplo: Adicionar Telegram

Este exemplo mostra como adicionar suporte para o Telegram ao middleware.

## Passo 1: Criar o Adaptador

Crie o arquivo `src/infrastructure/adapters/telegram/adapter.py`:

```python
"""Adaptador Telegram - Implementação para Telegram Bot API."""
from typing import Optional, Dict, Any
from datetime import datetime
import httpx

from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter
from src.domain.entities.message import Message, MessageType, MessageStatus


class TelegramAdapter(IMessagingPlatformAdapter):
    """
    Adaptador para Telegram Bot API.
    
    Implementa a interface IMessagingPlatformAdapter para comunicação
    com a API de bots do Telegram.
    """
    
    def __init__(self, bot_token: str):
        """
        Inicializa o adaptador Telegram.
        
        Args:
            bot_token: Token do bot do Telegram
        """
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(self, message: Message) -> bool:
        """Envia uma mensagem através do Telegram."""
        try:
            if message.message_type == MessageType.TEXT:
                return await self.send_text(message.recipient_id, message.content)
            return False
        except Exception:
            return False
    
    async def receive_message(self, webhook_data: Dict[str, Any]) -> Optional[Message]:
        """
        Processa webhook do Telegram e converte em Message.
        
        Args:
            webhook_data: Dados do webhook do Telegram
            
        Returns:
            Message ou None
        """
        try:
            # Estrutura do webhook do Telegram
            update = webhook_data.get("message", {})
            
            if not update:
                return None
            
            message_id = str(update.get("message_id"))
            sender_id = str(update.get("from", {}).get("id"))
            chat_id = str(update.get("chat", {}).get("id"))
            text = update.get("text", "")
            timestamp = datetime.fromtimestamp(update.get("date", 0))
            
            return Message(
                id=message_id,
                sender_id=sender_id,
                recipient_id=chat_id,
                content=text,
                message_type=MessageType.TEXT,
                platform="telegram",
                timestamp=timestamp,
                status=MessageStatus.DELIVERED,
                metadata=update
            )
        except Exception:
            return None
    
    async def send_text(self, recipient_id: str, text: str) -> bool:
        """
        Envia mensagem de texto via Telegram.
        
        Args:
            recipient_id: ID do chat
            text: Texto da mensagem
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            url = f"{self.api_url}/sendMessage"
            
            payload = {
                "chat_id": recipient_id,
                "text": text
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                return response.status_code == 200
        except Exception:
            return False
    
    async def send_interactive_message(
        self, 
        recipient_id: str, 
        text: str, 
        buttons: list
    ) -> bool:
        """
        Envia mensagem interativa com botões via Telegram.
        
        Args:
            recipient_id: ID do chat
            text: Texto da mensagem
            buttons: Lista de botões
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            url = f"{self.api_url}/sendMessage"
            
            # Formata botões para o formato do Telegram
            keyboard = []
            for button in buttons:
                keyboard.append([{"text": button, "callback_data": button}])
            
            payload = {
                "chat_id": recipient_id,
                "text": text,
                "reply_markup": {
                    "inline_keyboard": keyboard
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                return response.status_code == 200
        except Exception:
            return False
    
    def get_platform_name(self) -> str:
        """Retorna o nome da plataforma."""
        return "telegram"
    
    async def validate_webhook(self, request_data: Dict[str, Any]) -> bool:
        """
        Valida webhook do Telegram.
        
        Args:
            request_data: Dados da requisição
            
        Returns:
            bool: True se válido
        """
        # Validação básica - em produção, verificar secret token
        return "message" in request_data or "callback_query" in request_data
```

## Passo 2: Criar o __init__.py

Crie `src/infrastructure/adapters/telegram/__init__.py`:

```python
"""Adaptador Telegram."""
from .adapter import TelegramAdapter

__all__ = ["TelegramAdapter"]
```

## Passo 3: Criar o Webhook

Crie `src/interface/webhooks/telegram.py`:

```python
"""Webhook para Telegram."""
from fastapi import APIRouter, Request

from src.infrastructure.adapters.telegram import TelegramAdapter
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


def get_telegram_use_case() -> ProcessIncomingMessageUseCase:
    """Factory para criar o caso de uso com dependências."""
    adapter = TelegramAdapter(
        bot_token=settings.TELEGRAM_BOT_TOKEN
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


@router.post("/telegram")
async def telegram_webhook(request: Request):
    """
    Endpoint para receber mensagens do Telegram.
    
    Processa webhooks enviados pela API do Telegram.
    """
    try:
        body = await request.json()
        
        use_case = get_telegram_use_case()
        result = await use_case.execute(body)
        
        return {"success": True, "result": result}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Passo 4: Registrar no Router

Edite `src/interface/api/main.py` e adicione:

```python
from ..webhooks import telegram  # Adicione esta linha

# Na função create_app():
app.include_router(telegram.router, prefix="/api/v1/webhook", tags=["Telegram"])
```

## Passo 5: Adicionar Configurações

Edite `src/infrastructure/config/settings.py` e adicione:

```python
# Configurações do Telegram
TELEGRAM_BOT_TOKEN: str = ""
```

Edite `.env.example` e adicione:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

## Passo 6: Configurar o Webhook no Telegram

```bash
# Defina o webhook
curl -X POST "https://api.telegram.org/bot<SEU_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://seu-dominio.com/api/v1/webhook/telegram"}'

# Verifique o webhook
curl "https://api.telegram.org/bot<SEU_BOT_TOKEN>/getWebhookInfo"
```

## Passo 7: Testar

```bash
# 1. Configure o .env com o token do bot
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# 2. Execute o servidor
uv run python main.py

# 3. Envie uma mensagem para o bot no Telegram
# O middleware receberá, processará com Typebot e responderá!
```

## ✅ Pronto!

Seu middleware agora suporta Telegram! O mesmo padrão pode ser aplicado para:

- Discord
- Slack  
- Microsoft Teams
- LINE
- WeChat
- Qualquer outra plataforma!

## 🎯 Vantagens da Arquitetura

- **Sem alteração no código existente**: A lógica de negócio não muda
- **Mesmo fluxo**: Usa os mesmos use cases e serviços
- **Plug and play**: Basta criar o adaptador e registrar
- **Testável**: Pode ser testado independentemente
- **Manutenível**: Cada plataforma em seu próprio módulo
