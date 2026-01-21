"""Testes das entidades de domínio."""
import pytest
from datetime import datetime

from src.domain.entities.message import Message, MessageType, MessageStatus


class TestMessage:
    """Testes para a entidade Message."""
    
    def test_create_message_with_valid_data(self):
        """Testa criação de mensagem com dados válidos."""
        message = Message(
            id="msg_123",
            sender_id="user_456",
            recipient_id="bot_789",
            content="Olá, mundo!",
            message_type=MessageType.TEXT,
            platform="whatsapp",
            timestamp=datetime.now(),
            status=MessageStatus.PENDING
        )
        
        assert message.id == "msg_123"
        assert message.sender_id == "user_456"
        assert message.content == "Olá, mundo!"
        assert message.message_type == MessageType.TEXT
        assert message.platform == "whatsapp"
    
    def test_create_message_without_sender_id_raises_error(self):
        """Testa que criar mensagem sem sender_id levanta erro."""
        with pytest.raises(ValueError, match="sender_id não pode ser vazio"):
            Message(
                id="msg_123",
                sender_id="",
                recipient_id="bot_789",
                content="Olá",
                message_type=MessageType.TEXT,
                platform="whatsapp",
                timestamp=datetime.now()
            )
    
    def test_create_message_without_recipient_id_raises_error(self):
        """Testa que criar mensagem sem recipient_id levanta erro."""
        with pytest.raises(ValueError, match="recipient_id não pode ser vazio"):
            Message(
                id="msg_123",
                sender_id="user_456",
                recipient_id="",
                content="Olá",
                message_type=MessageType.TEXT,
                platform="whatsapp",
                timestamp=datetime.now()
            )
    
    def test_create_text_message_without_content_raises_error(self):
        """Testa que criar mensagem de texto sem conteúdo levanta erro."""
        with pytest.raises(ValueError, match="content não pode ser vazio para mensagens de texto"):
            Message(
                id="msg_123",
                sender_id="user_456",
                recipient_id="bot_789",
                content="",
                message_type=MessageType.TEXT,
                platform="whatsapp",
                timestamp=datetime.now()
            )
