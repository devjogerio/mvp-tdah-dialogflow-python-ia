# Pull Request: Atualização e Melhoria da Documentação (README.md)

**Título Sugerido:** `docs: update README with comprehensive project documentation`

## 📝 Descrição

Este PR realiza uma revisão completa e atualização do arquivo `README.md` para refletir o estado atual do projeto, incluindo as novas funcionalidades de automação do Dialogflow, arquitetura de IA e instruções detalhadas de configuração.

### 🔗 Issue Relacionada
Closes # (insira o número da issue se houver)

## 🛠️ Mudanças Realizadas

- **Visão Geral Expandida**: Detalhamento do propósito do MVP, focando em Saúde Mental, TDAH e suporte psicoeducativo.
- **Seção de Funcionalidades**:
  - Inclusão da Automação do Dialogflow ES (Intents/Entities via código).
  - Descrição da integração com AWS Bedrock e Llama 3.
  - Explicação sobre o sistema RAG (Retrieval-Augmented Generation).
- **Estrutura do Projeto**: Árvore de diretórios atualizada refletindo a nova organização (`src/dialogflow`, `docs/`, `infra/`).
- **Guia de Instalação**:
  - Passo a passo claro para setup de ambiente virtual e dependências.
  - Instruções específicas para configuração de variáveis de ambiente (`.env`).
- **Automação Dialogflow**: Nova seção explicando como executar o script `manager.py` para provisionar o agente.
- **Testes e Deploy**: Comandos atualizados para execução de testes e provisionamento de infraestrutura via Terraform.

## 📸 Demonstração (Excertos)

> "O sistema combina o poder da Inteligência Artificial Generativa (Llama 3 via Amazon Bedrock) com NLP estruturado (Dialogflow ES)..."

> "Para criar/atualizar Intents e Entities no Dialogflow baseando-se nos arquivos JSON em src/dialogflow/data/: python src/dialogflow/manager.py"

## ✅ Checklist de Revisão

- [x] O README descreve corretamente todas as funcionalidades implementadas?
- [x] As instruções de instalação foram testadas e funcionam em um ambiente limpo?
- [x] A estrutura de pastas documentada corresponde à realidade do repositório?
- [x] Não há informações sensíveis (chaves/senhas) expostas no texto?
- [x] A formatação Markdown está correta e legível?

## 👥 Revisores Sugeridos

- @tech-lead
- @product-owner
