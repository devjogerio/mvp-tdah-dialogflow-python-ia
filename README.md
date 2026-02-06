# Chatbot de Apoio à Saúde Mental (MVP)

Este projeto implementa um MVP de um chatbot inteligente e acolhedor para auxiliar pessoas com TDAH, ansiedade e depressão. O sistema utiliza Inteligência Artificial Generativa (Llama 3 via Amazon Bedrock) com técnica RAG (Retrieval-Augmented Generation) para fornecer informações baseadas em fontes clínicas confiáveis.

## 📋 Visão Geral

O objetivo é oferecer apoio psicoeducativo, triagem inteligente e uma interface adaptada para neurodivergentes.

### Funcionalidades Principais
- **Apoio Psicoeducativo**: Estratégias de manejo de sintomas.
- **Triagem de Crise**: Identificação de riscos e direcionamento para ajuda (CVV).
- **RAG**: Respostas fundamentadas em base de conhecimento clínica.
- **Segurança**: Filtros para prevenção de conteúdo nocivo.
- **Integração Dialogflow**: Automação completa de Intents, Entidades e Contextos.

## 🚀 Tecnologias

- **Linguagem**: Python 3.9+
- **Cloud**: AWS (Lambda, Bedrock, OpenSearch, S3), GCP (Dialogflow ES)
- **IA/LLM**: Meta Llama 3 (via Bedrock)
- **Frameworks**: Boto3, LangChain, google-cloud-dialogflow

## 📂 Estrutura do Projeto

```text
chatbot-saude-mental/
├── infra/            # Scripts de Infraestrutura (Terraform/CDK)
├── src/              # Código Fonte
│   ├── core/         # Lógica de Integração com Bedrock e RAG
│   ├── dialogflow/   # Automação e Gerenciamento do Dialogflow
│   │   ├── data/     # Definições JSON de Intents/Entidades
│   │   └── manager.py # Script de Automação
│   ├── utils/        # Utilitários e Filtros de Segurança
│   └── lambda_function.py # Entrypoint da AWS Lambda
├── data/             # Base de Conhecimento (Docs)
├── tests/            # Testes Unitários
└── requirements.txt  # Dependências
```

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.9 ou superior
- Conta AWS com permissões para Bedrock e Lambda
- Conta Google Cloud com Dialogflow API ativada
- Git

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/devjogerio/mvp-tdah-dialogflow-python-ia.git
   cd mvp-tdah-dialogflow-python-ia
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Copie o arquivo de exemplo:
     ```bash
     cp .env.example .env
     ```
   - Preencha o `.env` com suas credenciais AWS e GCP (`GOOGLE_APPLICATION_CREDENTIALS`).

## 🐳 Execução via Docker (Desenvolvimento Local)

O projeto conta com um ambiente Docker completo para facilitar o desenvolvimento local, simulando a infraestrutura AWS (OpenSearch) e encapsulando a Lambda em uma API REST local.

### Pré-requisitos
- Docker e Docker Compose instalados.

### Como Executar

1. **Configurar Variáveis**:
   Certifique-se de que o arquivo `.env` existe e contém suas credenciais AWS (necessárias para acessar o Bedrock na nuvem, já que ele não é mockado localmente):
   ```bash
   cp .env.example .env
   ```

2. **Iniciar o Ambiente**:
   ```bash
   docker-compose up --build
   ```

3. **Acessar Serviços**:
   - **API (Chatbot)**: http://localhost:8000/docs (Swagger UI)
   - **OpenSearch Dashboards**: http://localhost:5601
   - **OpenSearch API**: https://localhost:9200 (User: `admin`, Pass: `AdminStrongPass123!`)

### Detalhes da Estrutura Docker
- **app**: Container Python rodando a lógica da Lambda via FastAPI (hot-reload ativado).
- **opensearch**: Nó único do OpenSearch para RAG local.
- **opensearch-dashboards**: Interface visual para inspecionar índices e vetores.

### Testando o Chatbot Localmente
Envie uma requisição POST para `http://localhost:8000/chat` ou use o Swagger UI:
```json
{
  "message": "Como lidar com a ansiedade?"
}
```

## 🧪 Testes

Execute os testes unitários para validar a instalação:

```bash
pytest tests/
```

## 🤖 Automação Dialogflow

O projeto inclui um gerenciador automatizado para sincronizar Intents e Entidades com o Dialogflow ES.

### Configuração
1. Baixe a chave de serviço (JSON) do GCP.
2. Configure `GOOGLE_APPLICATION_CREDENTIALS` no `.env`.
3. Defina as intents em `src/dialogflow/data/initial_config.json`.

### Execução
```bash
# Sincronizar configuração local com a nuvem
python3 src/dialogflow/manager.py
```

## ⚙️ Automação e Deploy (Ops)

O projeto conta com uma ferramenta CLI para gerenciar testes, validação de infraestrutura e deploy.

### Uso do `deploy_manager.py`

O script `ops/deploy_manager.py` orquestra o pipeline de desenvolvimento.

```bash
# Executar validação completa e simular deploy em ambiente de desenvolvimento
python3 ops/deploy_manager.py --env dev

# Pular testes unitários
python3 ops/deploy_manager.py --env dev --skip-tests

# Simular deploy em produção
python3 ops/deploy_manager.py --env prod
```

O script gera logs detalhados em `deploy.log` e um relatório JSON ao final de cada execução.

## 🏗️ Infraestrutura como Código (IaC)
