"""Interface para integração com Typebot."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class ITypebotService(ABC):
    """
    Interface para serviço de integração com Typebot.
    
    Define o contrato para comunicação com a API do Typebot.
    """
    
    @abstractmethod
    async def send_message(
        self, 
        session_id: Optional[str],
        message: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Envia uma mensagem ao Typebot e recebe a resposta.
        
        Args:
            session_id: ID da sessão (None para nova sessão)
            message: Mensagem do usuário
            user_id: ID do usuário
            
        Returns:
            Dict contendo a resposta do Typebot e session_id
        """
        pass
    
    @abstractmethod
    async def start_conversation(self, user_id: str) -> Dict[str, Any]:
        """
        Inicia uma nova conversa no Typebot.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dict contendo session_id e mensagem inicial
        """
        pass
    
    @abstractmethod
    async def end_conversation(self, session_id: str) -> bool:
        """
        Finaliza uma conversa no Typebot.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            bool: True se finalizado com sucesso
        """
        pass
