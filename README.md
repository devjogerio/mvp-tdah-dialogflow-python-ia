# 🧠 Chatbot de Apoio à Saúde Mental (MVP)

Este projeto implementa um MVP de um assistente virtual inteligente e acolhedor, projetado para auxiliar pessoas com TDAH, ansiedade e depressão. O sistema combina o poder da **Inteligência Artificial Generativa (Multi-LLM: Bedrock, Gemini, OpenAI)** com **NLP estruturado (Dialogflow ES)** e técnica **RAG (Retrieval-Augmented Generation)** para fornecer suporte psicoeducativo, triagem de crises e estratégias de manejo baseadas em fontes clínicas confiáveis.

## 📋 Funcionalidades Principais

### 1. 💬 Interface & NLP (Dialogflow ES)

- **Conversação Natural**: Identificação precisa de intenções (Intents) e extração de entidades.
- **Automação Completa**: Criação e gerenciamento programático de Intents, Entities e Contextos via script Python.
- **Entidades Customizadas**: Reconhecimento de emoções e termos clínicos.
- **Gestão de Contexto**: Fluxos de conversa contínuos e coerentes.

### 2. 🧠 Inteligência Artificial (Multi-LLM)

- **Arquitetura Modular**: Suporte plugável para múltiplos provedores de LLM.
- **Provedores Suportados**:
  - **AWS Bedrock**: Llama 3 (padrão)
  - **Google Gemini**: Gemini Pro
  - **OpenAI**: GPT-3.5 / GPT-4
- **RAG (Retrieval-Augmented Generation)**: Enriquecimento das respostas com dados clínicos indexados no OpenSearch.
- **Filtros de Segurança**: Camada de proteção contra conteúdo nocivo ou inadequado.

### 3. 🛡️ Segurança & Infraestrutura

- **Segurança de Dados**: Credenciais gerenciadas via variáveis de ambiente e IAM Roles.
- **Infraestrutura como Código (IaC)**: Provisionamento automatizado via Terraform (EC2, S3, OpenSearch).
- **CI/CD**: Pipeline automatizado com GitHub Actions para testes e deploy.

## 🚀 Tecnologias Utilizadas

- **Linguagem Principal**: Python 3.9+
- **NLP/Chatbot**: Google Dialogflow ES v2
- **IA Generativa**: AWS Bedrock, Google Gemini, OpenAI
- **Busca Vetorial**: AWS OpenSearch Service
- **Computação Serverless**: AWS Lambda
- **Infraestrutura**: Terraform
- **Testes**: Pytest, Unittest.mock
- **Automação**: GitHub Actions

## 📂 Estrutura do Projeto

```text
chatbot-saude-mental/
├── .github/workflows/    # Pipelines de CI/CD
├── docs/                 # Documentação do projeto
├── infra/                # Módulos Terraform (Compute, Storage, Search)
├── ops/                  # Scripts de Operações e Deploy
├── src/                  # Código Fonte da Aplicação
│   ├── core/             # Integração com Bedrock e OpenSearch
│   ├── dialogflow/       # Automação e Gerenciamento do Dialogflow
│   │   ├── data/         # Configurações JSON (Intents/Entities)
│   │   └── manager.py    # Script de automação
│   ├── utils/            # Filtros de Segurança e Helpers
│   └── lambda_function.py # Entrypoint AWS Lambda
├── tests/                # Testes Unitários e de Integração
├── requirements.txt      # Dependências Python
└── README.md             # Documentação Principal
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.9+
- Conta Google Cloud (para Dialogflow)
- Conta AWS (para Bedrock/Lambda)
- Terraform (opcional, para infra)

### Passo a Passo

1. **Clone o repositório**

   ```bash
   git clone https://github.com/devjogerio/mvp-tdah-dialogflow-python-ia.git
   cd mvp-tdah-dialogflow-python-ia
   ```

2. **Crie e ative o ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração de Variáveis de Ambiente**
   Copie o arquivo de exemplo e preencha com suas credenciais:
   ```bash
   cp .env.example .env
   ```
   _Certifique-se de configurar `GOOGLE_APPLICATION_CREDENTIALS` e credenciais AWS._

## 🤖 Automação do Dialogflow

O projeto inclui um gerenciador automatizado para configurar seu agente Dialogflow.

### Executando a Automação

Para criar/atualizar Intents e Entities no Dialogflow baseando-se nos arquivos JSON em `src/dialogflow/data/`:

```bash
python src/dialogflow/manager.py
```

Isso irá:

1. Conectar ao projeto GCP configurado.
2. Criar entidades (ex: `Emotion`).
3. Criar intents (ex: `Welcome`, `Crisis Support`).
4. Configurar frases de treinamento e respostas.

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

O projeto utiliza `pytest` para garantir a qualidade do código.

```bash
# Executar todos os testes
pytest

# Executar apenas testes do Dialogflow
pytest tests/test_dialogflow.py
```

## 📦 Deploy da Infraestrutura

Para provisionar a infraestrutura na AWS:

```bash
cd infra
terraform init
terraform apply
```

## 🤝 Como Contribuir

1. Faça um Fork do projeto.
2. Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`).
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`).
4. Push para a Branch (`git push origin feature/MinhaFeature`).
5. Abra um Pull Request.

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
