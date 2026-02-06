# 🧠 Chatbot de Apoio à Saúde Mental (MVP)

![Build Status](https://img.shields.io/github/actions/workflow/status/devjogerio/mvp-tdah-dialogflow-python-ia/ci-cd.yml?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![AWS CDK](https://img.shields.io/badge/AWS%20CDK-2.0-orange?style=for-the-badge&logo=amazon-aws)
![Dialogflow](https://img.shields.io/badge/Dialogflow-ES-orange?style=for-the-badge&logo=google-cloud)
![License](https://img.shields.io/github/license/devjogerio/mvp-tdah-dialogflow-python-ia?style=for-the-badge)
![Version](https://img.shields.io/badge/release-v0.2.0-success?style=for-the-badge)

## 📖 Sobre o Projeto

O **Chatbot de Apoio à Saúde Mental** é uma solução digital empática e inteligente projetada para oferecer suporte inicial, psicoeducação e estratégias de coping para pessoas convivendo com TDAH, ansiedade e depressão.

Combinando a robustez do **Google Dialogflow ES** para compreensão de linguagem natural (NLU) com a flexibilidade da **IA Generativa (Llama 3 via Amazon Bedrock)** e técnicas de **RAG (Retrieval-Augmented Generation)**, este projeto visa democratizar o acesso a informações de saúde mental confiáveis e livres de julgamento.

> ⚠️ **Aviso Importante**: Este assistente é uma ferramenta de apoio e **não substitui** o diagnóstico ou tratamento médico profissional. Em casos de crise, o sistema é instruído a fornecer contatos de emergência (CVV 188).

---

## 🚀 Funcionalidades Principais

### 🗣️ Conversação Híbrida & Inteligente
- **NLU Estruturado (Dialogflow)**: Gestão precisa de intenções (Intents), entidades e contextos conversacionais para fluxos definidos.
- **IA Generativa (Fallback Inteligente)**: Quando o fluxo estruturado não cobre a dúvida do usuário, o modelo Llama 3 assume para gerar respostas contextualizadas e humanizadas.
- **RAG (Busca Semântica)**: Respostas embasadas em uma base de conhecimento clínica indexada (OpenSearch), reduzindo alucinações.

### 🔌 Arquitetura Resiliente (Adapter Pattern)
- **Normalização de Eventos**: Sistema agnóstico que aceita requisições via **Dialogflow Webhook** ou **API Gateway (REST)** através de um Adapter inteligente.
- **Gestão de Sessão**: Rastreabilidade completa de conversas para manutenção de contexto e análise futura.

### 🛠️ Automação de Infraestrutura (IaC & Ops)
- **Gerenciamento de Ciclo de Vida**: Scripts Python para criação e atualização (UPSERT) automática de Intents e Entities no Dialogflow.
- **AWS CDK**: Toda a infraestrutura (Lambda, DynamoDB, API Gateway) definida como código, facilitando réplicas de ambiente.
- **CI/CD**: Pipeline de integração contínua para testes e validação de qualidade.

---

## 🏗️ Stack Tecnológico

| Categoria | Tecnologia | Uso no Projeto |
| :--- | :--- | :--- |
| **Linguagem** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Lógica de backend, scripts de automação e testes. |
| **NLU / Chatbot** | ![Dialogflow](https://img.shields.io/badge/-Dialogflow-FF9800?logo=google-cloud&logoColor=white) | Processamento de linguagem natural e intenções. |
| **IA Generativa** | ![AWS Bedrock](https://img.shields.io/badge/-AWS%20Bedrock-232F3E?logo=amazon-aws&logoColor=white) | Acesso a LLMs (Llama 3, Titan) para geração de texto. |
| **Compute** | ![AWS Lambda](https://img.shields.io/badge/-AWS%20Lambda-FF9900?logo=aws-lambda&logoColor=white) | Execução serverless da lógica de negócios. |
| **Infraestrutura** | ![AWS CDK](https://img.shields.io/badge/-AWS%20CDK-8C4FFF?logo=amazon-aws&logoColor=white) | Definição e deploy de infraestrutura na AWS. |
| **Container** | ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white) | Ambiente de desenvolvimento consistente. |

---

## ⚡ Instalação e Uso

### Pré-requisitos
- Python 3.9+
- Conta AWS configurada (CLI)
- Conta Google Cloud (Service Account para Dialogflow)
- Docker (opcional, para ambiente isolado)

### 1. Clonar o Repositório
```bash
git clone https://github.com/devjogerio/mvp-tdah-dialogflow-python-ia.git
cd mvp-tdah-dialogflow-python-ia
```

### 2. Configurar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Configurar Variáveis de Ambiente
Duplique o arquivo de exemplo e preencha com suas chaves:
```bash
cp .env.example .env
```
> Edite o arquivo `.env` inserindo seu `GCP_PROJECT_ID` e credenciais AWS.

### 5. Sincronizar Dialogflow
Para carregar as Intents e Entities iniciais no seu agente Dialogflow:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
python src/dialogflow/manager.py
```

### 6. Executar Testes
```bash
pytest tests/
```

---

## 🚧 Status do Desenvolvimento

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=flat-square)

Atualmente na versão **v0.2.0**.
- [x] Estrutura base do projeto e CI/CD.
- [x] Integração AWS Lambda <-> Dialogflow (Webhook).
- [x] Implementação do Adapter Pattern para payloads.
- [x] Script de Automação (Manager) com lógica UPSERT.
- [ ] Persistência de Sessão (DynamoDB).
- [ ] Integração completa com RAG/OpenSearch (Em andamento).

---

## 🤝 Como Contribuir

Contribuições são super bem-vindas! Se você deseja melhorar este projeto:

1.  Faça um **Fork** do projeto.
2.  Crie uma **Branch** para sua feature (`git checkout -b feature/MinhaFeature`).
3.  Implemente suas mudanças e faça **Commit** (`git commit -m 'feat: Adiciona nova funcionalidade'`).
4.  Faça o **Push** (`git push origin feature/MinhaFeature`).
5.  Abra um **Pull Request**.

Por favor, certifique-se de atualizar os testes conforme necessário.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
  <sub>Desenvolvido com 💙 por <a href="https://github.com/devjogerio">Rogério Assunção</a></sub>
</div>
