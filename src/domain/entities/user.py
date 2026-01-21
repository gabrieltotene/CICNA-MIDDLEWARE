"""Entidade User - Representa um usuário do sistema."""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class User:
    """
    Entidade User.
    
    Representa um usuário que interage com o sistema através
    de diferentes plataformas de mensagens.
    """
    id: str
    name: str
    platform: str
    platform_user_id: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if not self.platform_user_id:
            raise ValueError("platform_user_id não pode ser vazio")
        if not self.platform:
            raise ValueError("platform não pode ser vazia")
