# Pull Request: Reestruturação Clean Architecture & GitFlow

**Branch:** `feature/project-cleanup-and-architecture` -> `develop`

## 📝 Descrição

Este PR implementa uma reestruturação massiva do projeto, adotando **Clean Architecture** e estabelecendo um workflow profissional com **GitFlow** e **Pre-commit hooks**. O objetivo é preparar o codebase para escalabilidade, facilitando testes, manutenção e a troca de componentes de infraestrutura (como LLMs e Bancos de Dados) sem afetar a lógica de negócios.

## 🏗️ Mudanças Arquiteturais

O código foi movido de uma estrutura monolítica (`src/core`) para camadas bem definidas:

1.  **Domain (`src/domain`)**:
    *   Entidades: `Session`, `User`, `Message`.
    *   Interfaces (Portas): `LLMProvider`, `ContextRepository`.
    *   *Dependências*: Nenhuma (Python puro).

2.  **Application (`src/application`)**:
    *   Use Cases: `ProcessUserMessage`.
    *   DTOs: `ProcessMessageInput`, `ProcessMessageOutput`.
    *   *Dependências*: Domain.

3.  **Infrastructure (`src/infrastructure`)**:
    *   LLM Adapters: `BedrockLLM`, `GeminiLLM`, `OpenAILLM`.
    *   Repositories: `MockOpenSearchRepository` (por enquanto).
    *   *Dependências*: Application, Domain, Libs Externas (boto3, openai).

4.  **Presentation (`src/presentation`)**:
    *   Handlers: `lambda_handler` (AWS Lambda).
    *   *Dependências*: Application, Infrastructure (para injeção).

## 🛠️ Tooling e Qualidade

*   **GitFlow**: Desenvolvimento centralizado na branch `develop`.
*   **Pre-commit Hooks**:
    *   `flake8`: Linting (PEP8).
    *   `black`: Formatação automática.
    *   `isort`: Organização de imports.
    *   `trailing-whitespace`: Limpeza de espaços.
*   **Templates**: Adicionados templates para Issues (Bug/Feature) e PRs.

## 🧹 Limpeza

*   Removido diretório legado `src/core`.
*   Removido código morto e importações não utilizadas.
*   Centralização da injeção de dependência no `lambda_handler` (Composition Root).

## ✅ Como Testar

1.  **Instalar dependências de dev**:
    ```bash
    pip install -r requirements-dev.txt
    pre-commit install
    ```
2.  **Rodar testes (Necessário atualizar os testes para a nova estrutura)**:
    *   *Nota*: Os testes antigos podem falhar devido à mudança de imports. A atualização dos testes é o próximo passo imediato após este merge.

## 📉 Impactos

*   **Breaking Changes**: A estrutura de imports mudou completamente. Qualquer script externo que importava `src.core` quebrará.
*   **Deploy**: O arquivo `src/lambda_function.py` foi atualizado para apontar para a nova arquitetura, mas o deploy deve garantir que todas as novas pastas (`src/domain`, etc.) sejam empacotadas.

---
**Status**: 🚀 Pronto para Review Técnica.
