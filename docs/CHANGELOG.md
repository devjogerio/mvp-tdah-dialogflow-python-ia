# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Novas Intents segmentadas para melhor fluxo conversacional:
  - `Sintomas Detalhados` (com contexto de entrada `tdah-info-context`)
  - `Acolhimento - Visão Geral` e `Acolhimento - Onde Ir` (flow de acolhimento)
  - `Tratamento - Medicamentos` e `Tratamento - Terapia TCC` (flow de tratamento)
  - `Dicas de Organização`
- Suporte a Contextos (Input/Output) e Lifespan no `DialogflowManager` e `initial_config.json`.
- Mais de 10 frases de treinamento para cada nova intent criada.

### Changed
- Refatoração completa de `initial_config.json`:
  - Fragmentação de respostas longas em múltiplas mensagens curtas (2-3 frases).
  - Decomposição de intents complexas (`TDAH Help`, `Acolhimento`, `Tratamento`) em fluxos contextuais.
  - Atualização de frases de treinamento existentes.
- Atualização do `DialogflowManager` para processar e sincronizar contextos de entrada e saída definidos no JSON.

### Deprecated
- 

### Removed
- 

### Fixed
- 

### Security
- 

## [0.2.0] - 2026-02-06

### Added
- **DialogflowAdapter**: Nova classe para normalização de payloads (Webhook Request vs API Gateway Event) garantindo compatibilidade entre diferentes fontes de entrada.
- **Mock de Credenciais**: Adicionado `credentials.json` (falso) e lógica de fallback para facilitar testes locais sem necessidade de chaves reais do GCP.
- **Documentação Técnica**: Relatórios completos de Correção, Execução e Análise do Ecossistema em `docs/DIALOGFLOW_TECHNICAL_REPORT.md`.

### Changed
- **DialogflowManager**: Atualizado para suportar lógica UPSERT (Update/Insert). Agora verifica existência de Intents e Entities antes de criar, realizando atualização se necessário.
- **Lambda Function**: Refatorada para utilizar o `DialogflowAdapter`, desacoplando a lógica de parsing da lógica de negócio.
- **Testes**: Suíte de testes atualizada para cobrir novos cenários de update e parsing de eventos.

### Fixed
- **Erro de Wrapper**: Removida classe interna inexistente `EntitiesBatch` na chamada de `batch_update_entities` da biblioteca `google-cloud-dialogflow`.
- **Testes de Integração**: Corrigida asserção em `test_create_entity` para validar chamada de `batch_update_entities` ao invés de criação duplicada.

## [0.1.0] - 2024-02-05

### Added
- Estrutura inicial do projeto.
- Integração com Amazon Bedrock (Mock).
- Filtros de segurança (Safety First).
- Testes unitários básicos.
- Pipeline de CI/CD inicial.
- Scripts de infraestrutura (Terraform).
