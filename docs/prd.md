# PRD - Chatbot de Apoio à Saúde Mental (TDAH, Ansiedade e Depressão)

## 1. Visão Geral

Este projeto visa criar um chatbot inteligente e acolhedor para auxiliar pessoas com TDAH, ansiedade e depressão. O sistema utiliza Inteligência Artificial Generativa (LLM) com a técnica de RAG (Geração Aumentada por Recuperação) para fornecer informações baseadas em fontes clínicas confiáveis.

## 2. Objetivos

- **Apoio Psicoeducativo:** Fornecer estratégias de manejo de sintomas.
- **Triagem Inteligente:** Identificar estados de crise e direcionar para ajuda profissional.
- **Acessibilidade:** Oferecer interface adaptada para neurodivergentes (respostas curtas e diretas).

## 3. Público-Alvo

- Indivíduos diagnosticados ou com suspeita de TDAH.
- Pessoas enfrentando episódios de ansiedade ou sintomas depressivos.
- Usuários que buscam uma interação de baixo custo cognitivo.

## 4. Arquitetura Técnica (Pillar AWS)

O sistema será construído sobre a infraestrutura da Amazon Web Services para garantir escalabilidade e segurança de dados.

| Componente        | Tecnologia                   | Função                                                       |
| :---------------- | :--------------------------- | :----------------------------------------------------------- |
| **Interface/NLP** | Dialogflow ES                | Gestão de intenções e fluxos de conversação iniciais.        |
| **Orquestração**  | AWS Lambda                   | Processamento lógico e integração entre APIs.                |
| **Cérebro (LLM)** | Amazon Bedrock (Llama 3)     | Geração de texto empático e contextual.                      |
| **Vector Store**  | Amazon OpenSearch Serverless | Armazenamento de embeddings para busca semântica.            |
| **Data Lake**     | Amazon S3                    | Repositório de documentos clínicos e manuais (PDF/Markdown). |

## 5. Requisitos Funcionais

### RF01: Processamento de Linguagem Natural (RAG)

O chatbot deve consultar uma base de conhecimento privada antes de responder, garantindo que as orientações sigam protocolos de saúde aprovados.

### RF02: Protocolo de Segurança (Safety First)

O sistema deve identificar palavras-chave de risco (suicídio, automutilação) e interromper o fluxo do LLM para exibir imediatamente contatos de emergência (CVV 188).

### RF03: Adaptação de Interface (UX para TDAH)

As respostas enviadas pelo modelo Llama 3 devem ser formatadas com:

- Uso de bullet points.
- Negrito em palavras-chave.
- Limite máximo de 3 parágrafos curtos.

## 6. Requisitos Não-Funcionais

- **Privacidade:** Os dados não devem ser utilizados para treinamento de modelos públicos (Garantido via Bedrock).
- **Latência:** O tempo de resposta total (incluindo RAG) não deve ultrapassar 4 segundos.
- **Disponibilidade:** A estrutura deve ser Serverless para garantir 99.9% de uptime.

## 7. Estrutura do Projeto (Repositório)

```text
chatbot-saude-mental/
├── infra/            # Terraform/CDK (S3, Bedrock, OpenSearch)
├── src/              # Python (Lambda Functions)
│   ├── core/         # Bedrock Integration & RAG Logic
│   └── utils/        # Formatters & Safety Filters
├── data/             # Knowledge Base (PDFs/MD)
└── tests/            # Unit & Integration Tests

8. Critérios de Sucesso
Acurácia do RAG: >90% das respostas devem conter informações extraídas dos documentos fornecidos.

Engajamento: Redução da taxa de abandono em fluxos de triagem longa.

Segurança: 100% de ativação do protocolo de emergência em testes de Red Teaming.

9. Riscos e Mitigações
Risco: Alucinação do LLM.

Mitigação: Implementação de Strict System Prompt e parametrização de temperatura baixa (0.1 - 0.2) no Llama 3.
```
