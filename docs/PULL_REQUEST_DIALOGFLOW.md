# Pull Request: Implementação da Automação Dialogflow ES

**Título Sugerido:** `feat: implement dialogflow automation and architecture`

## 📝 Descrição

Este PR implementa a arquitetura técnica completa para integração e automação do Dialogflow ES, permitindo o gerenciamento de Intents, Entidades e Contextos via código e arquivos de configuração JSON. A solução visa eliminar configurações manuais na interface do Dialogflow e garantir versionamento da lógica conversacional.

## 🛠️ Mudanças Realizadas

### 1. Módulo de Automação (`src/dialogflow/manager.py`)

- Implementado script Python utilizando `google-cloud-dialogflow` client library.
- **Funcionalidades**:
  - `create_intent`: Criação programática de intents com training phrases, mensagens e parâmetros.
  - `create_entity_type`: Criação de entidades customizadas com sinônimos.
  - `sync_from_json`: Leitura de configuração JSON para aplicar mudanças em massa.
  - `export_to_json`: Backup da configuração atual do agente para arquivo local.

### 2. Arquitetura de Arquivos (`src/dialogflow/data/`)

- Definido schema JSON (`initial_config.json`) para estruturar a base de conhecimento do chatbot.
- **Estrutura**:
  - `intents`: Lista de intents com prioridade, frases de treinamento e respostas.
  - `entities`: Definições de entidades (ex: Emotion) e seus valores.

### 3. Configuração e Dependências

- Adicionado `google-cloud-dialogflow` ao `requirements.txt`.
- Atualizado `README.md` com instruções de setup de credenciais GCP e execução da automação.
- **Gitignore Atualizado**: Adicionada regra para ignorar todos os arquivos `.md` exceto `README.md` (e este próprio arquivo se já rastreado), mantendo a documentação limpa.

### 4. Testes

- Criados testes unitários em `tests/test_dialogflow.py` utilizando `unittest.mock` para simular chamadas à API do Google, garantindo que o código funcione sem credenciais reais durante o CI.

## 📸 Demonstração

### Estrutura JSON (Exemplo)

```json
{
  "intents": [
    {
      "display_name": "TDAH Help",
      "training_phrases": ["O que é TDAH?"],
      "messages": [{ "text": ["O TDAH é um transtorno..."] }]
    }
  ]
}
```

### Execução da Automação

```bash
python3 src/dialogflow/manager.py
# Log:
# INFO:root:Entidade criada: Emotion
# INFO:root:Intent criada: Welcome Intent
# INFO:root:Intent criada: TDAH Help
```

## 🧪 Instruções de Teste

1. **Instalar Dependências**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Rodar Testes Unitários**:

   ```bash
   pytest tests/test_dialogflow.py
   ```

   _Resultado esperado: 3 testes passados._

3. **Teste Real (Opcional)**:
   - Configure `GOOGLE_APPLICATION_CREDENTIALS` no `.env`.
   - Execute `python3 src/dialogflow/manager.py`.
   - Verifique no console do Dialogflow se as intents foram criadas.

## ✅ Checklist de Pré-Merge

- [x] O código segue os padrões de estilo do projeto.
- [x] Testes unitários cobrindo criação de intents e entidades.
- [x] Documentação atualizada com novos comandos.
- [x] Arquitetura modular e extensível.

---

**Observação**: O sistema está pronto para ser conectado ao pipeline de CI/CD para deploy automático de mudanças no fluxo de conversa.
