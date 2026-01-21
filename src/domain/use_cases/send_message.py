"""Caso de uso: Enviar mensagem."""
from typing import Dict, Any
from ..entities.message import Message, MessageStatus
from ..interfaces.messaging_adapter import IMessagingPlatformAdapter
from ..interfaces.repositories import IMessageRepository


class SendMessageUseCase:
    """
    Caso de uso para enviar mensagens através de uma plataforma.
    
    Este caso de uso encapsula a lógica de negócio para envio de mensagens,
    independente da plataforma específica.
    """
    
    def __init__(
        self,
        messaging_adapter: IMessagingPlatformAdapter,
        message_repository: IMessageRepository
    ):
        self.messaging_adapter = messaging_adapter
        self.message_repository = message_repository
    
    async def execute(self, message: Message) -> Dict[str, Any]:
        """
        Executa o envio de uma mensagem.
        
        Args:
            message: Mensagem a ser enviada
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # Tenta enviar a mensagem
            success = await self.messaging_adapter.send_message(message)
            
            if success:
                message.status = MessageStatus.SENT
            else:
                message.status = MessageStatus.FAILED
            
            # Persiste a mensagem
            await self.message_repository.save(message)
            
            return {
                "success": success,
                "message_id": message.id,
                "status": message.status.value
            }
        except Exception as e:
            message.status = MessageStatus.FAILED
            await self.message_repository.save(message)
            
            return {
                "success": False,
                "message_id": message.id,
                "status": message.status.value,
                "error": str(e)
            }
