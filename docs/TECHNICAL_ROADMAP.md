# Roadmap Técnico: Projeto MVP TDAH Dialogflow Python

**Versão:** 1.0
**Data:** 07/02/2026
**Status:** Em Implementação

## 1. Visão Geral da Arquitetura Alvo

A arquitetura será migrada de um estilo "Service-Oriented" monolítico para uma **Clean Architecture (Onion Architecture)** estrita. O objetivo é desacoplar o núcleo de negócios (Domain) de frameworks externos (AWS Lambda, Dialogflow, Bancos de Dados).

### Diagrama de Camadas

```mermaid
graph TD
    Presentation[Presentation Layer\n(Lambda Handlers, API Controllers)] --> Application[Application Layer\n(Use Cases, DTOs, Ports)]
    Application --> Domain[Domain Layer\n(Entities, Value Objects, Repository Interfaces)]
    Infrastructure[Infrastructure Layer\n(Repositories Impl, External APIs, Adapters)] --> Domain
    Infrastructure --> Application
```

### Definição das Camadas

1.  **Domain (Núcleo)**:
    *   Entidades: `User`, `Session`, `Message`.
    *   Interfaces: `LLMProvider`, `SessionRepository`, `ContextRepository`.
    *   *Regra*: Zero dependências externas. Apenas Python puro.

2.  **Application (Orquestração)**:
    *   Use Cases: `ProcessUserMessage`, `AnalyzeRisk`.
    *   DTOs: `UserMessageInput`, `BotResponseOutput`.
    *   *Regra*: Implementa a lógica de aplicação usando as interfaces do Domain.

3.  **Infrastructure (Implementação)**:
    *   Adapters: `BedrockLLMAdapter`, `DialogflowAdapter`.
    *   Repositories: `DynamoDBSessionRepository`, `OpenSearchContextRepository`.
    *   *Regra*: Contém todo o código que toca em I/O, Bibliotecas de terceiros (boto3, google-cloud).

4.  **Presentation (Entrada)**:
    *   Handlers: `lambda_handler`.
    *   *Regra*: Recebe o evento bruto, converte para DTO, chama o Use Case e formata a resposta.

## 2. Padrões de Código e Qualidade

### Style Guide
- **Formatter**: Black (line-length 88).
- **Linter**: Flake8 (PEP8).
- **Imports**: isort (profile black).
- **Type Hinting**: Obrigatório em todas as assinaturas de função (mypy strict).

### Métricas de Qualidade
- **Cobertura de Testes**: Mínimo 80% (foco no Domain e Application).
- **Complexidade Ciclomática**: Máximo 10 por função.
- **Tamanho de Arquivo**: Máximo 300 linhas.
- **Tamanho de Função**: Máximo 20-30 linhas.

## 3. Processo de Review (Code Review)

Todo Pull Request deve passar por:
1.  **Pipeline Automatizado**: Lint, Tests, Security Scan.
2.  **Checklist Humano**:
    - [ ] Arquitetura respeitada (nenhuma violação de dependência entre camadas)?
    - [ ] Tratamento de erros adequado (exceções customizadas)?
    - [ ] Logs não expõem PII?
    - [ ] Testes cobrem os cenários de borda?

## 4. Cronograma de Refatoração

### Fase 1: Fundação (Atual)
- [x] Configuração GitFlow e Tooling.
- [ ] Criação da estrutura de pastas Clean Arch.
- [ ] Definição das Entidades e Interfaces do Domínio.

### Fase 2: Migração Core
- [ ] Refatorar `AssistantService` para Use Cases.
- [ ] Mover integrações (Bedrock/Gemini) para Infraestrutura.
- [ ] Implementar Injeção de Dependência manual.

### Fase 3: Limpeza e Otimização
- [ ] Remover código morto (`src/core` antigo).
- [ ] Otimizar Dockerfile e scripts de deploy.

## 5. Checklist de Deploy

- [ ] Variáveis de Ambiente configuradas (ver `.env.example`).
- [ ] Testes de Regressão passaram.
- [ ] Documentação de API (se houver) atualizada.
- [ ] Tag de versão criada (SemVer).
