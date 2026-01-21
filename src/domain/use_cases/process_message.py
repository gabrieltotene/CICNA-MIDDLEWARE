"""Caso de uso: Processar mensagem recebida."""
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from ..entities.user import User
from ..entities.message import Message, MessageType, MessageStatus
from ..entities.conversation import Conversation, ConversationStatus
from ..interfaces.messaging_adapter import IMessagingPlatformAdapter
from ..interfaces.typebot_service import ITypebotService
from ..interfaces.repositories import (
    IMessageRepository, 
    IUserRepository, 
    IConversationRepository
)


class ProcessIncomingMessageUseCase:
    """
    Caso de uso para processar mensagens recebidas.
    
    Este caso de uso orquestra o fluxo completo:
    1. Recebe mensagem da plataforma
    2. Identifica/cria usuário
    3. Gerencia conversa
    4. Envia ao Typebot
    5. Processa resposta do Typebot
    6. Envia resposta ao usuário
    """
    
    def __init__(
        self,
        messaging_adapter: IMessagingPlatformAdapter,
        typebot_service: ITypebotService,
        message_repository: IMessageRepository,
        user_repository: IUserRepository,
        conversation_repository: IConversationRepository
    ):
        self.messaging_adapter = messaging_adapter
        self.typebot_service = typebot_service
        self.message_repository = message_repository
        self.user_repository = user_repository
        self.conversation_repository = conversation_repository
    
    async def execute(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o processamento de uma mensagem recebida.
        
        Args:
            webhook_data: Dados do webhook da plataforma
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # 1. Converte webhook em Message
            incoming_message = await self.messaging_adapter.receive_message(webhook_data)
            
            if not incoming_message:
                return {"success": False, "error": "Não foi possível processar a mensagem"}
            
            # Salva a mensagem recebida
            incoming_message.status = MessageStatus.DELIVERED
            await self.message_repository.save(incoming_message)
            
            # 2. Identifica ou cria usuário
            user = await self.user_repository.get_by_platform_id(
                incoming_message.platform,
                incoming_message.sender_id
            )
            
            if not user:
                # Cria novo usuário (em produção, extrair mais dados do webhook)
                user = User(
                    id=f"{incoming_message.platform}_{incoming_message.sender_id}",
                    name="Usuário",
                    platform=incoming_message.platform,
                    platform_user_id=incoming_message.sender_id
                )
                await self.user_repository.save(user)
            
            # 3. Busca ou cria conversa ativa
            conversation = await self.conversation_repository.get_active_by_user(
                user.id,
                incoming_message.platform
            )
            
            if not conversation:
                # Cria nova conversa
                conversation = Conversation(
                    id=f"conv_{uuid.uuid4()}",
                    user_id=user.id,
                    platform=incoming_message.platform,
                    status=ConversationStatus.ACTIVE
                )
            
            conversation.add_message(incoming_message.id)
            await self.conversation_repository.save(conversation)
            
            # 4. Envia mensagem ao Typebot
            typebot_response = await self.typebot_service.send_message(
                session_id=conversation.typebot_session_id,
                message=incoming_message.content,
                user_id=user.id
            )
            
            # Atualiza session_id se necessário
            if typebot_response.get("session_id"):
                conversation.typebot_session_id = typebot_response["session_id"]
                await self.conversation_repository.save(conversation)
            
            # 5. Envia resposta ao usuário
            responses_sent = []
            for response_text in typebot_response.get("messages", []):
                success = await self.messaging_adapter.send_text(
                    incoming_message.sender_id,
                    response_text
                )
                
                # Cria registro da mensagem de resposta
                response_message = Message(
                    id=f"msg_{uuid.uuid4()}",
                    sender_id="system",
                    recipient_id=incoming_message.sender_id,
                    content=response_text,
                    message_type=MessageType.TEXT,
                    platform=incoming_message.platform,
                    timestamp=datetime.now(),
                    status=MessageStatus.SENT if success else MessageStatus.FAILED
                )
                await self.message_repository.save(response_message)
                conversation.add_message(response_message.id)
                
                responses_sent.append(success)
            
            await self.conversation_repository.save(conversation)
            
            return {
                "success": True,
                "message_id": incoming_message.id,
                "responses_sent": len(responses_sent),
                "all_responses_successful": all(responses_sent)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
