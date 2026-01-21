# CICNA Middleware

Middleware modular para conexão entre Typebot e plataformas de mensagens (WhatsApp, Instagram, Twitter).

## 📋 Sobre o Projeto

O CICNA Middleware é uma infraestrutura desenvolvida em Python que implementa **Clean Architecture** para conectar a API do Typebot com múltiplas plataformas de mensagens de forma modular e escalável.

### 🎯 Características Principais

- ✨ **Arquitetura Limpa**: Separação clara de responsabilidades em camadas
- 🔌 **Adaptadores Modulares**: Troca fácil entre plataformas (WhatsApp, Instagram, Twitter)
- 🚀 **Alta Performance**: Implementação assíncrona com FastAPI
- 📦 **Gerenciamento Moderno**: Uso de `uv` para gestão de dependências
- 🔒 **Segurança**: Validação de webhooks e autenticação
- 📊 **Monitoramento**: Logging estruturado e health checks

## 🏗️ Arquitetura

O projeto segue os princípios da **Clean Architecture**, dividido em 4 camadas principais:

```
src/
├── domain/              # Camada de Domínio
│   ├── entities/        # Entidades de negócio (Message, User, Conversation)
│   ├── interfaces/      # Contratos (Ports)
│   └── use_cases/       # Casos de uso
│
├── application/         # Camada de Aplicação
│   ├── services/        # Serviços (Typebot)
│   └── dto/            # Data Transfer Objects
│
├── infrastructure/      # Camada de Infraestrutura
│   ├── adapters/        # Adaptadores de plataformas
│   │   ├── whatsapp/   # Adaptador WhatsApp
│   │   ├── instagram/  # Adaptador Instagram
│   │   └── twitter/    # Adaptador Twitter
│   ├── repositories/    # Implementação de repositórios
│   └── config/         # Configurações
│
└── interface/          # Camada de Interface
    ├── api/            # API REST (FastAPI)
    └── webhooks/       # Endpoints de webhook
```

### 🔄 Fluxo de Dados

```
Plataforma (WhatsApp/Instagram/Twitter)
    ↓
Webhook (Interface Layer)
    ↓
ProcessIncomingMessageUseCase (Domain Layer)
    ↓
Typebot Service (Application Layer)
    ↓
Messaging Adapter (Infrastructure Layer)
    ↓
Resposta para o Usuário
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) instalado

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/gabrieltotene/CICNA-MIDDLEWARE.git
cd CICNA-MIDDLEWARE
```

2. **Instale o uv** (se ainda não tiver)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Instale as dependências**
```bash
uv sync
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. **Execute a aplicação**
```bash
uv run python main.py
```

A API estará disponível em `http://localhost:8000`

## ⚙️ Configuração

### Variáveis de Ambiente

Edite o arquivo `.env` com suas configurações:

```env
# Typebot
TYPEBOT_API_URL=https://typebot.io
TYPEBOT_ID=seu_typebot_id
TYPEBOT_API_TOKEN=seu_token_typebot

# WhatsApp
WHATSAPP_API_TOKEN=seu_token_whatsapp
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id
WHATSAPP_VERIFY_TOKEN=seu_verify_token

# Instagram
INSTAGRAM_ACCESS_TOKEN=seu_token_instagram
INSTAGRAM_PAGE_ID=seu_page_id

# Twitter
TWITTER_API_KEY=sua_api_key
TWITTER_API_SECRET=seu_api_secret
```

### Configuração de Webhooks

#### WhatsApp Business API

1. Acesse o [Meta for Developers](https://developers.facebook.com/)
2. Configure o webhook com a URL: `https://seu-dominio.com/api/v1/webhook/whatsapp`
3. Use o `WHATSAPP_VERIFY_TOKEN` configurado no `.env`

#### Instagram

1. Configure o webhook com a URL: `https://seu-dominio.com/api/v1/webhook/instagram`
2. (Em desenvolvimento)

#### Twitter

1. Configure o webhook com a URL: `https://seu-dominio.com/api/v1/webhook/twitter`
2. (Em desenvolvimento)

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

- `GET /api/v1/health` - Verificação de saúde da API
- `GET/POST /api/v1/webhook/whatsapp` - Webhook do WhatsApp
- `POST /api/v1/webhook/instagram` - Webhook do Instagram
- `POST /api/v1/webhook/twitter` - Webhook do Twitter

## 🔌 Adicionando Novas Plataformas

A arquitetura modular permite adicionar novas plataformas facilmente:

1. **Crie um novo adaptador** em `src/infrastructure/adapters/nova_plataforma/`
2. **Implemente a interface** `IMessagingPlatformAdapter`
3. **Crie o webhook** em `src/interface/webhooks/`
4. **Registre no router** em `src/interface/api/main.py`

### Exemplo de Novo Adaptador

```python
from src.domain.interfaces.messaging_adapter import IMessagingPlatformAdapter

class NovaPlataformaAdapter(IMessagingPlatformAdapter):
    async def send_message(self, message: Message) -> bool:
        # Implementação
        pass
    
    async def receive_message(self, webhook_data: Dict) -> Optional[Message]:
        # Implementação
        pass
    
    # ... outros métodos da interface
```

## 🧪 Testes

Execute os testes com:

```bash
# Todos os testes
uv run pytest

# Com cobertura
uv run pytest --cov=src --cov-report=html

# Testes específicos
uv run pytest tests/unit/
uv run pytest tests/integration/
```

## 🛠️ Desenvolvimento

### Ferramentas de Qualidade de Código

```bash
# Formatação com Black
uv run black src/

# Linting com Ruff
uv run ruff check src/

# Type checking com mypy
uv run mypy src/
```

### Estrutura de Commits

Use commits semânticos:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração
- `test:` Testes

## 📦 Dependências

### Principais

- **FastAPI**: Framework web assíncrono
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validação de dados
- **HTTPX**: Cliente HTTP assíncrono

### Desenvolvimento

- **pytest**: Framework de testes
- **black**: Formatação de código
- **ruff**: Linter
- **mypy**: Type checking

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Gabriel Totene** - [GitHub](https://github.com/gabrieltotene)

## 🙏 Agradecimentos

- [Typebot](https://typebot.io/) - Plataforma de chatbot
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [uv](https://github.com/astral-sh/uv) - Gerenciador de pacotes Python

---

Desenvolvido com ❤️ usando Python e Clean Architecture
