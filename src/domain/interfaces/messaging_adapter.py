"""Interface para adaptadores de plataformas de mensagens."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..entities.message import Message


class IMessagingPlatformAdapter(ABC):
    """
    Interface para adaptadores de plataformas de mensagens.
    
    Esta interface define o contrato que todos os adaptadores de plataformas
    (WhatsApp, Instagram, Twitter, etc) devem implementar, permitindo que
    a camada de aplicação funcione de forma agnóstica à plataforma específica.
    """
    
    @abstractmethod
    async def send_message(self, message: Message) -> bool:
        """
        Envia uma mensagem através da plataforma.
        
        Args:
            message: Mensagem a ser enviada
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso
        """
        pass
    
    @abstractmethod
    async def receive_message(self, webhook_data: Dict[str, Any]) -> Optional[Message]:
        """
        Processa dados de webhook e converte em uma mensagem.
        
        Args:
            webhook_data: Dados recebidos do webhook da plataforma
            
        Returns:
            Message ou None se não for possível processar
        """
        pass
    
    @abstractmethod
    async def send_text(self, recipient_id: str, text: str) -> bool:
        """
        Envia uma mensagem de texto simples.
        
        Args:
            recipient_id: ID do destinatário na plataforma
            text: Texto da mensagem
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso
        """
        pass
    
    @abstractmethod
    async def send_interactive_message(
        self, 
        recipient_id: str, 
        text: str, 
        buttons: list
    ) -> bool:
        """
        Envia uma mensagem interativa com botões.
        
        Args:
            recipient_id: ID do destinatário na plataforma
            text: Texto da mensagem
            buttons: Lista de botões
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso
        """
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """
        Retorna o nome da plataforma.
        
        Returns:
            str: Nome da plataforma (ex: "whatsapp", "instagram", "twitter")
        """
        pass
    
    @abstractmethod
    async def validate_webhook(self, request_data: Dict[str, Any]) -> bool:
        """
        Valida um webhook recebido da plataforma.
        
        Args:
            request_data: Dados da requisição
            
        Returns:
            bool: True se o webhook é válido
        """
        pass
