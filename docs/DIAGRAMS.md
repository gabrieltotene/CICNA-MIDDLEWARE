# Diagrama de Arquitetura - CICNA Middleware

## Fluxo Completo de Mensagem

```
┌──────────────────────────────────────────────────────────────────┐
│                    PLATAFORMAS DE MENSAGENS                      │
│         WhatsApp    Instagram    Twitter    [Outras...]          │
└────────────┬─────────────────────────────────────────────────────┘
             │
             │ Webhook HTTP
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER (API)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Webhook    │  │   Webhook    │  │   Webhook    │          │
│  │  WhatsApp    │  │  Instagram   │  │   Twitter    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │                  ▼                  │
          │        ┌─────────────────┐          │
          │        │   FastAPI App   │          │
          │        │  (Health Check) │          │
          │        └─────────────────┘          │
          │                                     │
          └─────────────────┬───────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER (Use Cases)                     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │     ProcessIncomingMessageUseCase                      │    │
│  │  1. Recebe mensagem da plataforma                      │    │
│  │  2. Identifica/cria usuário                            │    │
│  │  3. Gerencia conversa                                  │    │
│  │  4. Envia ao Typebot                                   │    │
│  │  5. Processa resposta                                  │    │
│  │  6. Envia resposta ao usuário                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │     SendMessageUseCase                                 │    │
│  │  1. Valida mensagem                                    │    │
│  │  2. Envia via adaptador                                │    │
│  │  3. Atualiza status                                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Message    │  │     User     │  │ Conversation │         │
│  │   (Entity)   │  │   (Entity)   │  │   (Entity)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────┬─────────────────────────────────────────────────────┘
            │
            │ Interfaces (Ports)
            ▼
┌─────────────────────────────────────────────────────────────────┐
│               INFRASTRUCTURE LAYER (Adapters)                   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Messaging Adapters                        │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │    │
│  │  │   WhatsApp   │  │  Instagram   │  │   Twitter   │  │    │
│  │  │   Adapter    │  │   Adapter    │  │   Adapter   │  │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Application Services                      │    │
│  │  ┌──────────────────────────────────────────────────┐  │    │
│  │  │           TypebotService                         │  │    │
│  │  │  - Gerencia sessões                              │  │    │
│  │  │  - Envia/recebe mensagens                        │  │    │
│  │  │  - Processa fluxos conversacionais               │  │    │
│  │  └──────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Repositories                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │    │
│  │  │   Message    │  │     User     │  │Conversation │  │    │
│  │  │ Repository   │  │ Repository   │  │ Repository  │  │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────┬───────────────────────────────────────┬───────────────┘
          │                                       │
          ▼                                       ▼
┌──────────────────────┐              ┌──────────────────────┐
│   Typebot API        │              │   Database           │
│   https://typebot.io │              │   (InMemory/SQL)     │
└──────────────────────┘              └──────────────────────┘
```

## Princípio de Dependência

```
┌─────────────────────────────────────────────────────────┐
│                    ALTA DEPENDÊNCIA                     │
│                    (Frameworks, UI)                     │
└─────────────────────────────────────────────────────────┘
                           │
                           │ depende de
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  CAMADA DE INTERFACE                    │
│                    (FastAPI, HTTP)                      │
└─────────────────────────────────────────────────────────┘
                           │
                           │ depende de
                           ▼
┌─────────────────────────────────────────────────────────┐
│                CAMADA DE INFRAESTRUTURA                 │
│          (Adaptadores, Repositórios, APIs)              │
└─────────────────────────────────────────────────────────┘
                           │
                           │ implementa interfaces de
                           ▼
┌─────────────────────────────────────────────────────────┐
│                 CAMADA DE APLICAÇÃO                     │
│                  (Serviços, DTOs)                       │
└─────────────────────────────────────────────────────────┘
                           │
                           │ usa
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   CAMADA DE DOMÍNIO                     │
│         (Entidades, Use Cases, Interfaces)              │
│                    NÚCLEO DO SISTEMA                    │
│                 (Lógica de Negócio Pura)                │
└─────────────────────────────────────────────────────────┘
```

## Modularidade das Plataformas

```
┌─────────────────────────────────────────────────────────┐
│              IMessagingPlatformAdapter                  │
│                    (Interface)                          │
│  + send_message(message: Message) -> bool              │
│  + receive_message(webhook_data) -> Message             │
│  + send_text(recipient, text) -> bool                   │
│  + send_interactive_message(...) -> bool                │
│  + validate_webhook(data) -> bool                       │
│  + get_platform_name() -> str                           │
└────────┬────────────────────────────────────┬───────────┘
         │                                    │
         │ implementa                         │ implementa
         ▼                                    ▼
┌──────────────────┐              ┌──────────────────┐
│  WhatsAppAdapter │              │ InstagramAdapter │
│                  │              │                  │
│ - Meta Graph API │              │ - Instagram API  │
│ - Envio de texto │              │ - (Estruturado)  │
│ - Botões         │              │                  │
│ - Webhooks       │              └──────────────────┘
└──────────────────┘
         │
         │ mesma interface
         ▼
┌──────────────────┐              ┌──────────────────┐
│  TwitterAdapter  │              │  TelegramAdapter │
│                  │              │                  │
│ - Twitter API    │              │ - Bot API        │
│ - (Estruturado)  │              │ - (Exemplo docs) │
└──────────────────┘              └──────────────────┘

💡 VANTAGEM: Trocar plataforma = trocar apenas o adaptador!
   Nenhuma mudança na lógica de negócio é necessária.
```

## Fluxo de Dados Detalhado

```
1. Usuário envia "Olá" pelo WhatsApp
   │
   ▼
2. Meta envia webhook para /api/v1/webhook/whatsapp
   │
   ▼
3. WhatsAppAdapter.receive_message() converte em Message
   │
   ▼
4. ProcessIncomingMessageUseCase.execute()
   ├─ UserRepository.get_by_platform_id()
   ├─ (se não existe) UserRepository.save(new User)
   ├─ ConversationRepository.get_active_by_user()
   ├─ (se não existe) ConversationRepository.save(new Conversation)
   │
   ▼
5. TypebotService.send_message("Olá", session_id, user_id)
   │
   ▼
6. Typebot processa e retorna: ["Olá! Como posso ajudar?"]
   │
   ▼
7. Para cada resposta:
   ├─ WhatsAppAdapter.send_text(recipient_id, resposta)
   ├─ MessageRepository.save(response_message)
   └─ Conversation.add_message(message_id)
   │
   ▼
8. Usuário recebe "Olá! Como posso ajudar?" no WhatsApp ✅
```

## Vantagens da Arquitetura

```
┌────────────────────────────────────────────────────────┐
│                  BENEFÍCIOS                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ✅ TESTABILIDADE                                      │
│     - Fácil criar mocks das interfaces                │
│     - Testes unitários isolados                       │
│     - Testes de integração por camada                 │
│                                                        │
│  ✅ MANUTENIBILIDADE                                   │
│     - Mudanças em uma camada não afetam outras        │
│     - Código organizado e fácil de encontrar          │
│     - Responsabilidades bem definidas                 │
│                                                        │
│  ✅ FLEXIBILIDADE                                      │
│     - Trocar WhatsApp por Telegram: apenas adaptador  │
│     - Mudar de InMemory para PostgreSQL: apenas repo  │
│     - Adicionar nova plataforma: sem alterar negócio  │
│                                                        │
│  ✅ ESCALABILIDADE                                     │
│     - Adicionar features sem quebrar existentes       │
│     - Suportar múltiplas plataformas simultaneamente  │
│     - Fácil horizontalizar (microserviços)            │
│                                                        │
│  ✅ INDEPENDÊNCIA                                      │
│     - Lógica de negócio não depende de frameworks     │
│     - Pode trocar FastAPI por Flask sem mudar core    │
│     - Typebot pode ser substituído sem refatoração    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

**Esta arquitetura garante que o código seja sustentável, testável e preparado para crescimento!** 🚀
