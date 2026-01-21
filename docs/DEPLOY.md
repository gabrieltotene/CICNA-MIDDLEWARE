# Guia de Deploy

## Deploy em Produção

### Requisitos

- Python 3.10+
- uv instalado
- Servidor com acesso à internet
- Domínio configurado com HTTPS

### 1. Preparação do Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python
sudo apt install python3.10 python3.10-venv -y

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Deploy da Aplicação

```bash
# Clonar repositório
git clone https://github.com/gabrieltotene/CICNA-MIDDLEWARE.git
cd CICNA-MIDDLEWARE

# Criar ambiente virtual e instalar dependências
uv sync

# Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Editar com suas credenciais
```

### 3. Executar com Systemd

Criar arquivo de serviço:

```bash
sudo nano /etc/systemd/system/cicna-middleware.service
```

Conteúdo:

```ini
[Unit]
Description=CICNA Middleware
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/CICNA-MIDDLEWARE
Environment="PATH=/caminho/para/CICNA-MIDDLEWARE/.venv/bin"
ExecStart=/caminho/para/CICNA-MIDDLEWARE/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cicna-middleware
sudo systemctl start cicna-middleware
sudo systemctl status cicna-middleware
```

### 4. Configurar Nginx como Reverse Proxy

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/cicna-middleware
```

Configuração:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ativar site:

```bash
sudo ln -s /etc/nginx/sites-available/cicna-middleware /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configurar HTTPS com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```

## Deploy com Docker

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar arquivos
COPY . .

# Instalar dependências
RUN uv sync

# Expor porta
EXPOSE 8000

# Comando de execução
CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  cicna-middleware:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: always
```

Executar:

```bash
docker-compose up -d
```

## Deploy na Nuvem

### Railway

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

### Heroku

```bash
# Login
heroku login

# Criar app
heroku create seu-app

# Configurar variáveis
heroku config:set TYPEBOT_API_URL=https://typebot.io
heroku config:set TYPEBOT_ID=seu_id

# Deploy
git push heroku main
```

### AWS EC2

1. Lançar instância EC2 (Ubuntu)
2. Configurar Security Groups (portas 80, 443)
3. Seguir passos de "Deploy em Produção"

### Google Cloud Run

```bash
# Build
gcloud builds submit --tag gcr.io/seu-projeto/cicna-middleware

# Deploy
gcloud run deploy cicna-middleware \
  --image gcr.io/seu-projeto/cicna-middleware \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Monitoramento

### Logs

```bash
# Ver logs do systemd
sudo journalctl -u cicna-middleware -f

# Ver logs do Docker
docker-compose logs -f
```

### Health Check

```bash
curl https://seu-dominio.com/api/v1/health
```

## Backup e Recuperação

### Backup de Dados

```bash
# Backup do banco de dados (quando implementado)
# pg_dump ou mongodump

# Backup de configurações
cp .env .env.backup
```

## Segurança

### Checklist

- [ ] Usar HTTPS (certificado SSL)
- [ ] Configurar firewall
- [ ] Usar secrets manager para credenciais
- [ ] Atualizar dependências regularmente
- [ ] Implementar rate limiting
- [ ] Configurar logging adequado
- [ ] Fazer backups regulares

### Firewall (UFW)

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

## Troubleshooting

### Aplicação não inicia

1. Verificar logs: `sudo journalctl -u cicna-middleware -n 50`
2. Verificar variáveis de ambiente
3. Verificar permissões

### Webhook não funciona

1. Verificar URL pública
2. Verificar HTTPS
3. Verificar logs da plataforma
4. Testar endpoint manualmente

### Performance

1. Usar Gunicorn com múltiplos workers
2. Configurar cache
3. Otimizar queries de banco de dados
4. Usar CDN para assets
