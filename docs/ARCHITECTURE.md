# Documentação da Arquitetura

## Visão Geral

O CICNA Middleware implementa uma **Clean Architecture** (Arquitetura Limpa) para garantir:

- Independência de frameworks
- Testabilidade
- Independência de UI
- Independência de banco de dados
- Independência de agentes externos

## Camadas da Arquitetura

### 1. Camada de Domínio (Domain Layer)

**Localização**: `src/domain/`

A camada mais interna, que contém a lógica de negócio pura.

#### Entidades (`entities/`)
- **Message**: Representa uma mensagem no sistema
- **User**: Representa um usuário
- **Conversation**: Representa uma conversa

#### Interfaces (`interfaces/`)
Define contratos (Ports) que devem ser implementados pelas camadas externas:
- `IMessagingPlatformAdapter`: Interface para adaptadores de plataformas
- `ITypebotService`: Interface para serviço Typebot
- `IMessageRepository`, `IUserRepository`, `IConversationRepository`: Interfaces de repositórios

#### Casos de Uso (`use_cases/`)
- **SendMessageUseCase**: Envia mensagens através de uma plataforma
- **ProcessIncomingMessageUseCase**: Processa mensagens recebidas

### 2. Camada de Aplicação (Application Layer)

**Localização**: `src/application/`

Orquestra o fluxo de dados entre a camada de domínio e as camadas externas.

#### Serviços (`services/`)
- **TypebotService**: Implementação da integração com Typebot

### 3. Camada de Infraestrutura (Infrastructure Layer)

**Localização**: `src/infrastructure/`

Implementa os detalhes técnicos e se comunica com serviços externos.

#### Adaptadores (`adapters/`)
Implementações concretas das interfaces de mensagens:

- **WhatsAppAdapter**: Integração com WhatsApp Business API
  - Envia mensagens de texto
  - Envia mensagens interativas (botões)
  - Processa webhooks do WhatsApp
  
- **InstagramAdapter**: Integração com Instagram Messaging API (em desenvolvimento)
- **TwitterAdapter**: Integração com Twitter API (em desenvolvimento)

#### Repositórios (`repositories/`)
- **InMemoryRepository**: Implementação em memória para desenvolvimento/testes
- (Futuro: PostgreSQL, MongoDB, etc.)

#### Configuração (`config/`)
- **Settings**: Gerenciamento de configurações usando Pydantic

### 4. Camada de Interface (Interface Layer)

**Localização**: `src/interface/`

Ponto de entrada da aplicação, expõe a API REST.

#### API (`api/`)
- **main.py**: Configuração da aplicação FastAPI
- **health.py**: Endpoint de health check

#### Webhooks (`webhooks/`)
- **whatsapp.py**: Webhook para WhatsApp
- **instagram.py**: Webhook para Instagram
- **twitter.py**: Webhook para Twitter

## Fluxo de Dados

### Mensagem Recebida (Incoming)

```
1. Webhook recebe dados da plataforma (Interface Layer)
   ↓
2. ProcessIncomingMessageUseCase é executado (Domain Layer)
   ↓
3. Adaptador converte webhook em Message (Infrastructure Layer)
   ↓
4. Repositórios persistem dados (Infrastructure Layer)
   ↓
5. TypebotService processa mensagem (Application Layer)
   ↓
6. Adaptador envia resposta para plataforma (Infrastructure Layer)
```

### Mensagem Enviada (Outgoing)

```
1. SendMessageUseCase é executado (Domain Layer)
   ↓
2. Adaptador envia mensagem via API da plataforma (Infrastructure Layer)
   ↓
3. Repositório persiste status da mensagem (Infrastructure Layer)
```

## Princípios Aplicados

### Dependency Inversion Principle (DIP)
As camadas internas não dependem das externas. As dependências apontam para dentro.

```python
# Domain define a interface
class IMessagingPlatformAdapter(ABC):
    async def send_message(self, message: Message) -> bool:
        pass

# Infrastructure implementa
class WhatsAppAdapter(IMessagingPlatformAdapter):
    async def send_message(self, message: Message) -> bool:
        # Implementação específica
```

### Interface Segregation Principle (ISP)
Interfaces específicas para cada responsabilidade.

### Single Responsibility Principle (SRP)
Cada classe tem uma única responsabilidade:
- Entidades: Representam conceitos de negócio
- Use Cases: Orquestram fluxos de negócio
- Adapters: Adaptam interfaces externas
- Repositories: Gerenciam persistência

## Vantagens desta Arquitetura

1. **Testabilidade**: Fácil criar mocks e stubs das interfaces
2. **Manutenibilidade**: Mudanças em uma camada não afetam outras
3. **Flexibilidade**: Trocar implementações (ex: WhatsApp por Telegram) sem alterar lógica de negócio
4. **Escalabilidade**: Adicionar novas plataformas é simples
5. **Clareza**: Separação clara de responsabilidades

## Como Adicionar Uma Nova Plataforma

### Passo 1: Criar o Adaptador

```python
# src/infrastructure/adapters/telegram/adapter.py
from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter

class TelegramAdapter(IMessagingPlatformAdapter):
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
    
    async def send_message(self, message: Message) -> bool:
        # Implementação específica do Telegram
        pass
    
    async def receive_message(self, webhook_data: Dict) -> Optional[Message]:
        # Converte webhook do Telegram para Message
        pass
    
    # ... outros métodos
```

### Passo 2: Criar o Webhook

```python
# src/interface/webhooks/telegram.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    # Processa webhook do Telegram
    use_case = get_telegram_use_case()
    result = await use_case.execute(await request.json())
    return result
```

### Passo 3: Registrar no Router

```python
# src/interface/api/main.py
from ..webhooks import telegram

app.include_router(telegram.router, prefix="/api/v1/webhook", tags=["Telegram"])
```

### Passo 4: Adicionar Configurações

```python
# src/infrastructure/config/settings.py
class Settings(BaseSettings):
    # ...
    TELEGRAM_BOT_TOKEN: str = ""
```

**Pronto!** A nova plataforma está integrada sem modificar a lógica de negócio existente.
