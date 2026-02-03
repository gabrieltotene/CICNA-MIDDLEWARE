"""Serviço de integração com Typebot."""
from typing import Optional, Dict, Any
import httpx

from src.domain.interfaces.typebot_service import ITypebotService


class TypebotService(ITypebotService):
    """
    Implementação do serviço de integração com Typebot.
    
    Gerencia a comunicação com a API do Typebot para processamento
    de conversas e fluxos conversacionais.
    """
    
    def __init__(self, api_url: str, typebot_id: str, api_token: Optional[str] = None):
        """
        Inicializa o serviço Typebot.
        
        Args:
            api_url: URL da API do Typebot
            typebot_id: ID do bot no Typebot
            api_token: Token de autenticação (opcional)
        """
        self.api_url = api_url.rstrip("/")
        self.typebot_id = typebot_id
        self.api_token = api_token
        self.headers = {}
        
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
    
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
        try:
            # Constrói URL baseado se é nova sessão ou continuação
            if session_id:
                url = f"{self.api_url}/api/v1/sessions/{session_id}/continueChat"
            else:
                url = f"{self.api_url}/api/v1/typebots/{self.typebot_id}/startChat"
            
            payload = {
                "message": message,
            }

            if not session_id:
                payload["prefilledVariables"] = {
                    "userId": user_id
                }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    print("Typebot response data:", data)
                    # Extrai mensagens do Typebot com validação
                    messages = []
                    for msg in data.get("messages", []):
                        if msg.get("type") == "text":
                            # Acesso seguro aos dados aninhados
                            content = msg.get("content", {})
                            rich_text = content.get("richText", [])
                            if rich_text and len(rich_text) > 0:
                                children = rich_text[0].get("children", [])
                                if children and len(children) > 0:
                                    text = children[0].get("text", "")
                                    if text:
                                        messages.append(text)
                    if data.get("input")["type"] == "choice input":
                        items = data.get("input")["items"]
                        print("Choice input items:", items)
                        # for item in items:
                        #     messages.append(f"{item.get('content', '')}")
                        messages.append(items)

                    print("Extracted messages from Typebot:", messages)

                    return {
                        "session_id": data.get("sessionId", session_id),
                        "messages": messages,
                        "success": True
                    }
                else:
                    return {
                        "session_id": session_id,
                        "messages": ["Desculpe, ocorreu um erro ao processar sua mensagem."],
                        "success": False
                    }
        except Exception as e:
            return {
                "session_id": session_id,
                "messages": [f"Erro ao comunicar com Typebot: {str(e)}"],
                "success": False
            }
    
    async def start_conversation(self, user_id: str) -> Dict[str, Any]:
        """
        Inicia uma nova conversa no Typebot.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dict contendo session_id e mensagem inicial
        """
        return await self.send_message(None, "", user_id)
    
    async def end_conversation(self, session_id: str) -> bool:
        """
        Finaliza uma conversa no Typebot.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            bool: True se finalizado com sucesso
        """
        # Typebot geralmente não requer finalização explícita
        # Implementar se necessário
        return True
