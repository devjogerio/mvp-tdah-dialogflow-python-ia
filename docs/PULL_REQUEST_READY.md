# Pull Request: Implementação de Arquitetura Multi-LLM (Bedrock, Gemini, OpenAI)

**Título:** feat(core): implement modular multi-LLM architecture supporting Bedrock, Gemini, and OpenAI

## 📝 Descrição

Esta PR introduz uma refatoração arquitetural significativa no núcleo do assistente, substituindo a dependência direta do Amazon Bedrock por uma arquitetura modular baseada em interfaces (`LLMProvider`). Isso permite que o sistema alterne dinamicamente entre diferentes provedores de Inteligência Artificial Generativa (Llama 3 via Bedrock, Google Gemini Pro e OpenAI GPT) através de variáveis de ambiente, aumentando a resiliência e evitando vendor lock-in.

### 🎯 Motivação e Impacto

*   **Flexibilidade**: Capacidade de escolher o modelo com melhor custo-benefício ou performance para cada ambiente.
*   **Resiliência**: Preparação para estratégias de fallback (ex: se Bedrock cair, usar OpenAI).
*   **Modernização**: Adição de suporte aos modelos mais recentes do mercado (Gemini 1.5, GPT-4).
*   **Manutenibilidade**: Desacoplamento da lógica de negócio (`AssistantService`) da implementação específica do modelo.

## 🛠️ Mudanças Principais

1.  **Nova Interface `LLMProvider`**: Contrato abstrato para interação com LLMs.
2.  **Factory Pattern (`LLMFactory`)**: Criação centralizada de instâncias de LLM baseada na env `LLM_PROVIDER`.
3.  **Novos Adaptadores**:
    *   `src/core/llm/bedrock.py`: Adaptador para AWS Bedrock (Llama 3).
    *   `src/core/llm/gemini.py`: Adaptador para Google Gemini.
    *   `src/core/llm/openai.py`: Adaptador para OpenAI.
4.  **Refatoração do `lambda_function.py`**: Migração para usar `AssistantService` em vez de `BedrockService`.
5.  **Resolução de Conflitos**: Merge da branch `develop` resolvendo conflitos em `manager.py` e `README.md`.

## ✅ Checklist de Validação

- [x] **Testes Unitários**: Novos testes criados para `LLMFactory` e `AssistantService`.
- [x] **Testes de Integração**: Validação do fluxo completo no `lambda_function`.
- [x] **Linting**: Código verificado com `flake8`.
- [x] **Retrocompatibilidade**: O comportamento padrão (Bedrock) foi preservado.
- [x] **Documentação**: Atualização do `README.md` e `TECHNICAL_ANALYSIS_REPORT.md`.

## 📸 Evidências

### 1. Sucesso nos Testes Automatizados
```bash
tests/test_core.py ...                                                [ 12%]
tests/test_dialogflow.py ...                                          [ 24%]
tests/test_lambda.py ..                                               [ 32%]
tests/test_lambda_dialogflow.py ..                                    [ 40%]
tests/test_llm_factory.py ....                                        [ 56%]
...
====================== 25 passed, 3 warnings in 7.38s =======================
```

### 2. Estrutura de Diretórios Nova
```text
src/core/
├── assistant_service.py  <-- Novo Orquestrador
├── llm/
│   ├── base.py           <-- Interface
│   ├── factory.py        <-- Fábrica
│   ├── bedrock.py
│   ├── gemini.py
│   └── openai.py
```

## ⚠️ Análise de Riscos

*   **Risco Baixo**: A mudança é puramente backend e protegida por feature flags (via variável de ambiente).
*   **Dependências**: Novas libs adicionadas (`google-generativeai`, `openai`). Verifique o tamanho do pacote Lambda se for crítico.
*   **Configuração**: É necessário adicionar as chaves `GEMINI_API_KEY` ou `OPENAI_API_KEY` no `.env` para usar os novos provedores.

## 🔄 Instruções para Revisores

1.  Verificar se a lógica de retry do `manager.py` (vinda da develop) foi mantida corretamente.
2.  Validar se a interface `LLMProvider` cobre todos os casos de uso atuais.
3.  Sugerir melhorias na gestão de erros dos novos provedores.

---
**PR criada automaticamente pelo Assistente de Arquitetura Trae AI.**
