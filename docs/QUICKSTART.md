# Início Rápido - CICNA Middleware

## 🚀 Começando em 5 minutos

### 1. Instalar uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip (alternativa)
pip install uv
```

### 2. Clonar e Configurar

```bash
# Clone o repositório
git clone https://github.com/gabrieltotene/CICNA-MIDDLEWARE.git
cd CICNA-MIDDLEWARE

# Instale as dependências
uv sync

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

### 3. Executar

```bash
# Desenvolvimento
uv run python main.py

# Ou com reload automático
uv run uvicorn src.interface.api.main:app --reload

# Testes
uv run pytest
```

### 4. Acessar

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/v1/health

## 📝 Configuração Mínima

Edite o `.env`:

```env
# Typebot (obrigatório)
TYPEBOT_API_URL=https://typebot.io
TYPEBOT_ID=seu_typebot_id
TYPEBOT_API_TOKEN=seu_token

# WhatsApp (opcional, mas recomendado)
WHATSAPP_API_TOKEN=seu_token_whatsapp
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id
WHATSAPP_VERIFY_TOKEN=seu_verify_token
```

## 🔌 Testar WhatsApp Webhook

```bash
# 1. Configure o webhook no Meta for Developers:
URL: https://seu-dominio.com/api/v1/webhook/whatsapp
Verify Token: (o valor configurado no .env)

# 2. Teste localmente com ngrok:
ngrok http 8000

# 3. Use a URL do ngrok no webhook do Meta
```

## 📚 Próximos Passos

- [Documentação Completa](README.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Deploy](docs/DEPLOY.md)

## 🆘 Problemas Comuns

### uv não encontrado
```bash
# Adicione ao PATH (Linux/macOS)
export PATH="$HOME/.cargo/bin:$PATH"
```

### Porta 8000 em uso
```bash
# Altere no .env
PORT=8080
```

### Imports não funcionam
```bash
# Reinstale as dependências
uv sync --reinstall
```

## 💡 Dicas

- Use `uv run` antes de todos os comandos Python
- Configure o `.env` antes de executar
- Teste a API com `/docs` (Swagger UI)
- Veja logs em tempo real no console

---

**Pronto!** Seu middleware está rodando! 🎉
