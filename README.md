# Chatbot de Apoio à Saúde Mental (MVP)

Este projeto implementa um MVP de um chatbot inteligente e acolhedor para auxiliar pessoas com TDAH, ansiedade e depressão. O sistema utiliza Inteligência Artificial Generativa (Llama 3 via Amazon Bedrock) com técnica RAG (Retrieval-Augmented Generation) para fornecer informações baseadas em fontes clínicas confiáveis.

## 📋 Visão Geral

O objetivo é oferecer apoio psicoeducativo, triagem inteligente e uma interface adaptada para neurodivergentes.

### Funcionalidades Principais
- **Apoio Psicoeducativo**: Estratégias de manejo de sintomas.
- **Triagem de Crise**: Identificação de riscos e direcionamento para ajuda (CVV).
- **RAG**: Respostas fundamentadas em base de conhecimento clínica.
- **Segurança**: Filtros para prevenção de conteúdo nocivo.

## 🚀 Tecnologias

- **Linguagem**: Python 3.9+
- **Cloud**: AWS (Lambda, Bedrock, OpenSearch, S3)
- **IA/LLM**: Meta Llama 3 (via Bedrock)
- **Frameworks**: Boto3, LangChain

## 📂 Estrutura do Projeto

```text
chatbot-saude-mental/
├── infra/            # Scripts de Infraestrutura (Terraform/CDK)
├── src/              # Código Fonte
│   ├── core/         # Lógica de Integração com Bedrock e RAG
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
   - Preencha o `.env` com suas credenciais AWS.

## 🧪 Testes

Execute os testes unitários para validar a instalação:

```bash
pytest tests/
```

## 📦 Deploy

O deploy é realizado via GitHub Actions (CI/CD) ou manualmente via AWS CLI/Terraform (detalhes na pasta `infra/`).

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/IncrivelFeature`)
3. Faça o Commit (`git commit -m 'Add some IncrivelFeature'`)
4. Faça o Push (`git push origin feature/IncrivelFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
