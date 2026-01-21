"""Repositórios em memória para desenvolvimento e testes."""
from typing import Optional, List, Dict
from src.domain.entities.message import Message
from src.domain.entities.user import User
from src.domain.entities.conversation import Conversation, ConversationStatus
from src.domain.interfaces.repositories import (
    IMessageRepository,
    IUserRepository,
    IConversationRepository
)


class InMemoryMessageRepository(IMessageRepository):
    """Repositório de mensagens em memória."""
    
    def __init__(self):
        self._messages: Dict[str, Message] = {}
    
    async def save(self, message: Message) -> Message:
        """Salva uma mensagem."""
        self._messages[message.id] = message
        return message
    
    async def get_by_id(self, message_id: str) -> Optional[Message]:
        """Busca uma mensagem por ID."""
        return self._messages.get(message_id)
    
    async def get_by_conversation(self, conversation_id: str) -> List[Message]:
        """Busca mensagens de uma conversa."""
        # Implementação simplificada
        return []


class InMemoryUserRepository(IUserRepository):
    """Repositório de usuários em memória."""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._platform_index: Dict[str, User] = {}
    
    async def save(self, user: User) -> User:
        """Salva um usuário."""
        self._users[user.id] = user
        key = f"{user.platform}:{user.platform_user_id}"
        self._platform_index[key] = user
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário por ID."""
        return self._users.get(user_id)
    
    async def get_by_platform_id(self, platform: str, platform_user_id: str) -> Optional[User]:
        """Busca um usuário por ID da plataforma."""
        key = f"{platform}:{platform_user_id}"
        return self._platform_index.get(key)


class InMemoryConversationRepository(IConversationRepository):
    """Repositório de conversas em memória."""
    
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
    
    async def save(self, conversation: Conversation) -> Conversation:
        """Salva uma conversa."""
        self._conversations[conversation.id] = conversation
        return conversation
    
    async def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Busca uma conversa por ID."""
        return self._conversations.get(conversation_id)
    
    async def get_active_by_user(self, user_id: str, platform: str) -> Optional[Conversation]:
        """Busca conversa ativa de um usuário."""
        for conv in self._conversations.values():
            if (conv.user_id == user_id and 
                conv.platform == platform and 
                conv.status == ConversationStatus.ACTIVE):
                return conv
        return None
