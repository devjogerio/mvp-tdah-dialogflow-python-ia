# 🚀 Processo de Release e Deploy

Este documento descreve o fluxo de trabalho para versionamento, testes e deploy do projeto **MVP TDAH Dialogflow**.

## 🔄 Fluxo de Desenvolvimento (GitFlow)

1.  **Feature Branch**:
    - Crie uma branch a partir de `main` (ou `develop`) seguindo o padrão: `feature/nome-da-funcionalidade`.
    - Exemplo: `git checkout -b feature/auto-understanding-system main`

2.  **Commits**:
    - Utilize **Conventional Commits**:
      - `feat: nova funcionalidade`
      - `fix: correção de bug`
      - `docs: documentação`
      - `refactor: melhoria de código sem alterar comportamento`
      - `test: adição ou correção de testes`

3.  **Pull Request (PR)**:
    - Abra um PR para `main` (ou `develop`).
    - Preencha o template de PR com:
      - Descrição das mudanças.
      - Checklist de validação.
      - Links para issues/tickets.
    - **CI/CD Automático**: O GitHub Actions rodará testes e linting automaticamente.

4.  **Code Review**:
    - Necessário pelo menos 1 aprovação.
    - Todos os checks do CI devem passar.

5.  **Merge**:
    - Após aprovação, faça o merge (Squash and Merge recomendado para manter histórico limpo).

## 🤖 CI/CD Pipeline

O pipeline está configurado em `.github/workflows/ci-cd.yml` e executa:

1.  **Testes (`test` job)**:
    - Instala dependências (`requirements.txt` e `requirements-dev.txt`).
    - Executa Linting (`flake8`).
    - Valida configurações do Dialogflow (`validate_config.py`).
    - Executa Testes Unitários (`pytest`).

2.  **Validação de Infra (`cdk-check` job)**:
    - Instala AWS CDK.
    - Executa `cdk synth` para validar templates de infraestrutura.

3.  **Deploy (`deploy-dev` / `deploy-prod`)**:
    - **Dev**: Automático ao mergear na branch `develop`.
    - **Prod**: Automático ao criar uma tag `v*` (ex: `v1.0.0`).

## 🛡️ Proteção de Branch

Recomendações configuradas no repositório:

- **Require pull request reviews before merging**: 1 aprovação.
- **Require status checks to pass before merging**: `test` e `cdk-check` devem passar.

## 📝 Padrões de Documentação

- **Localização**: Todos os arquivos de documentação (`.md`) devem ser salvos na pasta `docs/` ou em seus subdiretórios.
  - Exceção: `README.md` (Raiz) e `.github/` templates.
- **Validação**: O pipeline de CI verifica automaticamente se há arquivos `.md` fora dos diretórios permitidos.

## 📦 Checklist de Release

Antes de criar uma release de produção:

- [ ] Atualizar `docs/CHANGELOG.md`.
- [ ] Verificar se `initial_config.json` está atualizado e validado.
- [ ] Garantir que documentação técnica reflete mudanças.
- [ ] Criar tag git: `git tag -a v1.X.X -m "Release v1.X.X" && git push origin v1.X.X`.
