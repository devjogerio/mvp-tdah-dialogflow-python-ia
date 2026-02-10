# Pull Request: Feature Multi-LLM Support

## Título
`feat: implement modular LLM architecture with Gemini and OpenAI support`

## Descrição Detalhada

Esta mudança introduz uma arquitetura modular para provedores de Large Language Models (LLM), permitindo que o sistema utilize não apenas o Amazon Bedrock (Llama 3), mas também o Google Gemini e a OpenAI (GPT).

### Motivação
A dependência única do Amazon Bedrock limitava a flexibilidade do projeto e criava um ponto único de falha. A nova arquitetura permite:
1.  **Redundância**: Possibilidade de fallback entre provedores.
2.  **Custo/Performance**: Escolha do modelo mais adequado para cada ambiente ou caso de uso.
3.  **Evolução**: Facilidade para adicionar novos modelos futuros (ex: Anthropic Claude direto, Mistral, etc.).

### Mudanças Realizadas
-   **Nova Arquitetura (`src/core/llm/`)**:
    -   Criada interface abstrata `LLMProvider`.
    -   Implementados provedores concretos: `BedrockLLM`, `GeminiLLM`, `OpenAILLM`.
    -   Implementado `LLMFactory` para instanciar o provedor correto baseado na env var `LLM_PROVIDER`.
-   **Refatoração de Serviço**:
    -   `BedrockService` foi substituído por `AssistantService` (`src/core/assistant_service.py`), que orquestra a chamada ao LLM e ao RAG.
    -   `lambda_function.py` atualizado para usar `AssistantService`.
-   **Testes**:
    -   Adicionados testes unitários para a Factory (`tests/test_llm_factory.py`).
    -   Atualizados testes existentes (`test_core.py`, `test_lambda.py`) para usar mocks da nova arquitetura.
-   **Documentação**:
    -   Atualizado `README.md` com novas capacidades.
    -   Atualizado `.env.example` com novas variáveis de configuração.
    -   Relatório técnico detalhado em `docs/TECHNICAL_ANALYSIS_REPORT.md`.

## Checklist de Testes Realizados

- [x] **Testes Unitários**:
    - `tests/test_llm_factory.py`: Validação da criação correta de providers (Bedrock, Gemini, OpenAI) e fallback.
    - `tests/test_core.py`: Validação do `AssistantService` e integração com RAG mockado.
    - `tests/test_lambda.py`: Validação do handler Lambda com a nova abstração.
    - Resultado: 23 testes passaram (`pytest` executado com sucesso).
- [x] **Análise Estática**:
    - Verificação de imports e estrutura de pacotes.
- [x] **Validação de Build**:
    - Instalação de novas dependências (`google-generativeai`, `openai`) verificada.

## Evidências de Funcionamento

### Logs de Testes
```bash
tests/test_core.py ...                                                       [ 13%]
tests/test_dialogflow.py ...                                                 [ 26%]
tests/test_lambda.py ..                                                      [ 34%]
tests/test_lambda_dialogflow.py ..                                           [ 43%]
tests/test_llm_factory.py ....                                               [ 60%]
tests/test_manager.py ...                                                    [ 73%]
tests/test_opensearch.py ...                                                 [ 86%]
tests/test_safety.py ...                                                     [100%]
========================== 23 passed, 1 warning in 7.71s ===========================
```

## Análise de Riscos e Breaking Changes

### Breaking Changes
-   **Remoção de Arquivo**: `src/core/bedrock_integration.py` foi removido. Qualquer código externo que importasse `BedrockService` diretamente quebrará. (Mitigado: O projeto é autocontido e todas as referências internas foram atualizadas).
-   **Variáveis de Ambiente**: O comportamento padrão continua sendo Bedrock, mas para usar outros modelos, novas variáveis (`GEMINI_API_KEY`, `OPENAI_API_KEY`) são obrigatórias.

### Riscos
-   **Dependências**: Novas bibliotecas (`google-generativeai`, `openai`) aumentam o tamanho do pacote de deploy do Lambda. Pode ser necessário ajustar o tamanho da Layer ou container Docker se o limite for atingido.
-   **Latência**: A latência de rede para APIs externas (Google/OpenAI) pode variar em comparação ao Bedrock (que roda dentro da VPC AWS se configurado via PrivateLink, ou na mesma região).

## Solicitação de Revisão
Solicito revisão focada em:
1.  Robustez do tratamento de erros nos novos providers (`src/core/llm/*.py`).
2.  Clareza da abstração no `AssistantService`.
