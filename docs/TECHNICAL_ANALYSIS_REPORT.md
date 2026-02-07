# Relatório de Análise Técnica: MVP TDAH Dialogflow Python

**Data:** 07/02/2026  
**Versão do Documento:** 1.0  
**Autor:** Assistente de Arquitetura de Software (Trae AI)

---

## 1. Visão Geral e Arquitetura

O projeto consiste em um backend serverless para um chatbot de saúde mental focado em TDAH, integrado ao Google Dialogflow e utilizando Inteligência Artificial Generativa (RAG + LLM) via Amazon Bedrock.

### Estrutura de Diretórios

A organização do projeto segue boas práticas de separação de responsabilidades:

- **`src/core/`**: Lógica de negócios central (integração com LLM e Vector DB).
- **`src/dialogflow/`**: Adaptadores e gerenciadores específicos para o ecossistema Dialogflow.
- **`src/utils/`**: Utilitários transversais (ex: filtros de segurança).
- **`src/lambda_function.py`**: Ponto de entrada (Entrypoint) da AWS Lambda.
- **`infra/`**: Código de Infraestrutura como Código (IaC) com AWS CDK.
- **`tests/`**: Testes unitários bem estruturados.
- **`ops/` & `scripts/`**: Automação de deploy e manutenção.
- **`docs/`**: Documentação centralizada.

### Fluxo de Dados

1.  **Entrada**: Webhook do Dialogflow ou API Gateway aciona o Lambda.
2.  **Adaptação**: `DialogflowAdapter` normaliza o payload.
3.  **Segurança**: `safety_filters.py` analisa o input em busca de riscos.
4.  **Recuperação (RAG)**: `BedrockService` consulta o `OpenSearchService` para contexto (atualmente mockado/simulado).
5.  **Geração**: `BedrockService` invoca o modelo Llama 3 no Amazon Bedrock.
6.  **Resposta**: O texto gerado é formatado e retornado ao Dialogflow.

---

## 2. Análise de Qualidade de Código

### Pontos Fortes

- **Modularidade**: O código é desacoplado. É possível trocar o provedor de vetor ou de LLM sem reescrever o adaptador do Dialogflow.
- **Padrões de Projeto**: Uso claro de _Adapter Pattern_ (`DialogflowAdapter`) e _Service Layer_ (`BedrockService`, `OpenSearchService`).
- **Tratamento de Erros**: O `lambda_handler` possui blocos `try-except` robustos com respostas de fallback seguras.
- **Type Hinting**: Uso consistente de tipos (`typing`) facilita a leitura e previne erros.

### Débitos Técnicos e Code Smells

1.  **Mock de RAG (`src/core/bedrock_integration.py`)**:
    - O método `retrieve_context` possui um vetor de embedding _hardcoded_ (`[0.1] * 1536`) e um fallback de texto fixo. Isso impede o funcionamento real da busca semântica.
    - _Impacto_: Crítico para a funcionalidade de resposta contextual.
2.  **Filtro de Segurança Simplista (`src/utils/safety_filters.py`)**:
    - Baseado apenas em RegEx e palavras-chave. Falha em detectar nuances ou tentativas de contorno (_jailbreak_).
    - _Impacto_: Risco de segurança e responsabilidade em um app de saúde mental.
3.  **Dependências Desatualizadas**:
    - `requirements.txt` lista `langchain==0.1.0` e `boto3==1.34.0`. Bibliotecas de IA evoluem rápido; versões antigas podem perder features de performance e segurança.
4.  **Sincronismo Bloqueante**:
    - As chamadas para OpenSearch e Bedrock são síncronas. Em picos de latência da AWS, o Dialogflow pode sofrer _timeout_ (limite padrão de 5s).

---

## 3. Segurança e Performance

### Segurança

- **Segredos**: O projeto usa corretamente variáveis de ambiente (`os.getenv`), evitando credenciais hardcoded.
- **Validação de Input**: O `DialogflowAdapter` faz parse seguro, mas não há sanitização profunda contra injeção de prompt (_Prompt Injection_).
- **Dados Sensíveis**: Não há ofuscação de PII (Personal Identifiable Information) nos logs antes de enviar para o CloudWatch.

### Performance

- **Cold Starts**: Python em Lambda pode ter _cold starts_ de 2-5 segundos, o que é perigoso para o timeout do Dialogflow.
- **Reuso de Conexão**: O cliente `boto3` é inicializado fora do handler, o que é excelente para performance.

---

## 4. Sugestões de Melhorias (Roadmap)

### Fase 1: Correções Críticas (Curto Prazo)

- [ ] **Implementar Embedding Real**: Substituir o vetor mockado em `retrieve_context` por uma chamada ao modelo `amazon.titan-embed-text-v1` ou similar.
- [ ] **Atualizar Dependências**: Revisar e atualizar `boto3`, `langchain` e `opensearch-py`.
- [ ] **Sanitização de Logs**: Garantir que mensagens de usuários (potencialmente sensíveis) não sejam logadas em texto plano se não for estritamente necessário para debug.

### Fase 2: Robustez e Funcionalidade (Médio Prazo)

- [ ] **Memória de Conversação**: Implementar persistência de contexto (DynamoDB ou Redis) para que o bot lembre do que foi dito anteriormente na sessão.
- [ ] **Melhoria no Filtro de Segurança**: Integrar o _Llama Guard_ ou usar a API de _Guardrails_ do Amazon Bedrock para filtragem mais inteligente.
- [ ] **Tratamento de Timeout**: Implementar um mecanismo de "keep-alive" ou respostas assíncronas se o processamento do LLM exceder 4 segundos.

### Fase 3: Expansão (Longo Prazo)

- [ ] **Painel Administrativo**: Interface para terapeutas/admins revisarem conversas sinalizadas como risco.
- [ ] **Testes de Carga**: Validar o comportamento da infraestrutura sob alto volume de requisições.

---

## 5. Propostas de Novas Features

### Feature A: Memória de Sessão (Contexto Conversacional)

- **Descrição**: Permitir que o bot mantenha o contexto de perguntas anteriores (ex: "E quais são os sintomas?" após "O que é TDAH?").
- **Valor**: Torna a conversa natural e fluida.
- **Complexidade**: Média (Requer DynamoDB/ElastiCache).

### Feature B: Dashboard de Insights

- **Descrição**: Visualização de tópicos mais perguntados, taxa de detecção de risco e feedback de usuários.
- **Valor**: Ajuda a melhorar o conteúdo da base de conhecimento.
- **Complexidade**: Alta (Requer API separada + Frontend).

## 6. Atualização de Arquitetura (Multi-LLM)

### Visão Geral da Mudança

Implementação de suporte a múltiplos provedores de LLM (Amazon Bedrock, Google Gemini, OpenAI) através de uma arquitetura modular baseada em interfaces.

### Mudanças Realizadas

1.  **Interface Abstrata (`LLMProvider`)**: Define o contrato `invoke(prompt, context)` que todos os provedores devem implementar.
2.  **Implementações Concretas**:
    - `BedrockLLM`: Mantém a integração existente com AWS Bedrock (Llama 3).
    - `GeminiLLM`: Nova integração com Google Gemini Pro.
    - `OpenAILLM`: Nova integração com OpenAI GPT-3.5/4.
3.  **Factory Pattern (`LLMFactory`)**: Centraliza a criação de instâncias baseada na variável de ambiente `LLM_PROVIDER`.
4.  **AssistantService**: Substitui o antigo `BedrockService` (agora obsoleto e removido), atuando como orquestrador entre RAG e a Factory de LLM.

### Benefícios

- **Flexibilidade**: Troca de modelo/provedor apenas alterando variáveis de ambiente (`LLM_PROVIDER`, `GEMINI_API_KEY`, etc.), sem deploy de código.
- **Resiliência**: Facilita a implementação de estratégias de fallback (ex: se Bedrock falhar, tentar OpenAI).
- **Testabilidade**: A arquitetura desacoplada facilita o mock de provedores nos testes unitários.

### Próximos Passos (Específicos da Feature)

- [ ] Adicionar testes de integração reais para cada provedor (com chaves de teste).
- [ ] Implementar fallback automático na Factory em caso de falha de um provedor.
- **Valor**: Dados para refinar o RAG e o prompt do sistema.
- **Complexidade**: Baixa (Webhook handler para eventos de feedback).

---

## 6. Conclusão

O projeto possui uma base arquitetural sólida e bem organizada. O principal ponto de atenção é a implementação "mockada" do RAG, que precisa ser finalizada para que o produto entregue valor real. Com as correções de embedding e melhorias de segurança sugeridas, a solução estará pronta para um MVP robusto.
