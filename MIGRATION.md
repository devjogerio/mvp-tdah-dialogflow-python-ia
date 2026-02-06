# Migração de Terraform para AWS CDK (Python)

Este documento detalha o processo de migração da infraestrutura do projeto, anteriormente gerenciada por Terraform, para AWS Cloud Development Kit (CDK) em Python.

## 🔄 Visão Geral da Mudança

A infraestrutura foi migrada para AWS CDK para alinhar o gerenciamento de infraestrutura com a linguagem principal do projeto (Python), permitindo maior flexibilidade, type safety e uso de construtos de alto nível.

### Recursos Migrados

| Recurso Terraform | Construto CDK (Python) | Nome Lógico |
|-------------------|------------------------|-------------|
| AWS S3 Bucket     | `s3.Bucket`            | `Storage/KnowledgeBaseBucket` |
| OpenSearch Coll.  | `oss.CfnCollection`    | `Search/KbCollection` |
| Lambda Function   | `lambda.Function`      | `Compute/ChatbotLambda` |

## 🛠️ Pré-requisitos

1.  Node.js (para CLI do CDK)
2.  Python 3.9+
3.  Credenciais AWS configuradas

## 🚀 Como Deployar (Nova Estrutura)

1.  Instale o AWS CDK CLI:
    ```bash
    npm install -g aws-cdk
    ```

2.  Instale as dependências Python:
    ```bash
    cd infra
    pip install -r requirements.txt
    ```

3.  Sintetize o template CloudFormation (Validação):
    ```bash
    cdk synth
    ```

4.  Deploy:
    ```bash
    cdk deploy
    ```

## ⚠️ Processo de Migração (Importante)

Como esta é uma substituição de IaC para recursos existentes, existem dois caminhos:

### Cenário A: Infraestrutura NÃO Provisionada (Ambiente Novo)
Basta rodar `cdk deploy`. O CDK criará todos os recursos do zero.

### Cenário B: Infraestrutura JÁ Provisionada (Produção)
Para evitar recriar recursos (o que causaria perda de dados no S3 ou downtime), deve-se usar o comando `cdk import` ou garantir que os recursos Terraform sejam removidos do estado mas não destruídos na nuvem (`terraform state rm`), e então importados para o CloudFormation.

**Passo a Passo para Importação (Zero Downtime):**

1.  Certifique-se que o Terraform não destruiu os recursos (use `terraform destroy` APENAS se for ambiente de teste descartável). Se for produção, apenas delete os arquivos `.tf`.
2.  Execute o deploy do CDK. Se o recurso já existir com o mesmo nome físico, o CloudFormation pode falhar informando "Resource already exists".
3.  Nesse caso, use o comando de importação:
    ```bash
    cdk import TdahChatbotStack
    ```
    O CDK identificará os recursos existentes pelos nomes físicos definidos no código (`mvp-tdah-kb-docs`, `tdah-knowledge`, etc.) e os associará à stack do CloudFormation.

## ✅ Validação Pós-Migração

1.  Verifique se o Bucket S3 `mvp-tdah-kb-docs` mantém seus arquivos.
2.  Verifique se a função Lambda `tdah-chatbot-handler` está ativa e com a role correta.
3.  Teste o endpoint do OpenSearch Serverless.

## 🔙 Rollback

Caso a migração falhe:
1.  Reverta a branch para `main` (onde estão os arquivos Terraform).
2.  Execute `terraform init` e `terraform plan` para garantir que o Terraform reconhece o estado atual (assumindo que o `terraform.tfstate` remoto não foi corrompido).
