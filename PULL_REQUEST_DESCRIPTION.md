# Feature: Auto-Understanding System & Versioning Setup

## 🎯 Objetivo
Implementar um sistema de autoaprendizado para o chatbot baseado em documentos Markdown e estabelecer um pipeline robusto de CI/CD para versionamento e deploy.

## 🛠️ Mudanças Realizadas

### 🧠 Auto-Understanding System
- **Parser (`markdown_parser.py`)**: Implementado parser que converte arquivos Markdown de estudos de caso em Intents e Entities do Dialogflow.
- **Migration Script (`migrate_case_study.py`)**: Script para atualização automática (upsert) do `initial_config.json` com novos conhecimentos extraídos.
- **Validação (`validate_config.py`)**: Validador de schema para garantir integridade da configuração do Dialogflow.
- **Testes**: Adicionados testes unitários para o parser.
- **Documentação**: Criado `docs/technical/AUTO_UNDERSTANDING_SYSTEM.md`.

### 🔄 CI/CD & Versionamento
- **Workflow GitHub Actions (`ci-cd.yml`)**:
    - Adicionado passo de **Linting** (`flake8`).
    - Adicionado passo de **Validação de Config** (`validate_config.py`).
    - Otimizada instalação de dependências.
- **Documentação de Processo**: Criado `docs/RELEASE_PROCESS.md` detalhando o fluxo de GitFlow e Deploy.
- **Template de PR**: Criado `.github/PULL_REQUEST_TEMPLATE.md`.

### 🧹 Limpeza e Refatoração
- **Clean Code**: Remoção de arquivos não utilizados (`generate_resume.py`, logs antigos).
- **Dependências**: Separação clara entre `requirements.txt` (prod) e `requirements-dev.txt` (dev/test).
- **Correções**: Fix de imports não utilizados em diversos arquivos core.

## 🧪 Validação
- [x] **Testes Unitários**: `python -m unittest tests/test_markdown_parser.py` (Passou)
- [x] **Linting**: Código verificado com flake8.
- [x] **Migração**: `migrate_case_study.py` executado com sucesso, atualizando `initial_config.json`.
- [x] **Config Check**: `validate_config.py` validou o JSON final com sucesso.

## 🔗 Issues Relacionadas
- Closes #TASK-1 (Markdown Parser)
- Closes #TASK-2 (CI/CD Setup)

---
**Tipo de Mudança**:
- [x] ✨ Nova Funcionalidade (feat)
- [x] 🏗️ Infraestrutura / CI (chore)
- [x] 📝 Documentação (docs)
