"""Interfaces de repositórios."""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.message import Message
from ..entities.user import User
from ..entities.conversation import Conversation


class IMessageRepository(ABC):
    """Interface para repositório de mensagens."""
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        """Salva uma mensagem."""
        pass
    
    @abstractmethod
    async def get_by_id(self, message_id: str) -> Optional[Message]:
        """Busca uma mensagem por ID."""
        pass
    
    @abstractmethod
    async def get_by_conversation(self, conversation_id: str) -> List[Message]:
        """Busca mensagens de uma conversa."""
        pass


class IUserRepository(ABC):
    """Interface para repositório de usuários."""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Salva um usuário."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário por ID."""
        pass
    
    @abstractmethod
    async def get_by_platform_id(self, platform: str, platform_user_id: str) -> Optional[User]:
        """Busca um usuário por ID da plataforma."""
        pass


class IConversationRepository(ABC):
    """Interface para repositório de conversas."""
    
    @abstractmethod
    async def save(self, conversation: Conversation) -> Conversation:
        """Salva uma conversa."""
        pass
    
    @abstractmethod
    async def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Busca uma conversa por ID."""
        pass
    
    @abstractmethod
    async def get_active_by_user(self, user_id: str, platform: str) -> Optional[Conversation]:
        """Busca conversa ativa de um usuário."""
        pass
