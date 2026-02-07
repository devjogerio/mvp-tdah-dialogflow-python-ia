# Pull Request: Implementação de Automação de Deploy do Dialogflow

## Resumo
Este PR introduz um script de automação robusto (`scripts/deploy_intents.sh`) e melhorias no gerenciador Python (`src/dialogflow/manager.py`) para permitir a sincronização automática de intents e entidades do arquivo de configuração JSON para o console do Dialogflow.

## Alterações Principais

### 1. Script de Automação (`scripts/deploy_intents.sh`)
- **Configuração de Ambiente**: Define automaticamente `GOOGLE_APPLICATION_CREDENTIALS` e `PYTHONPATH`.
- **Compatibilidade**: Exporta `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` para mitigar problemas com Python 3.x recentes.
- **Resiliência**: Implementa lógica de retry (3 tentativas) com backoff exponencial no nível do shell.
- **Validação**: Verifica a existência do arquivo de chave JSON e do script Python antes da execução.
- **Logging**: Fornece logs coloridos e detalhados de cada etapa.

### 2. Melhorias no Gerenciador (`src/dialogflow/manager.py`)
- **Tratamento de Erros**: Adicionado bloco `try-except` específico para `DefaultCredentialsError` e `ValueError` na inicialização, fornecendo mensagens de erro amigáveis se a chave for inválida.
- **Modo Standalone**: O módulo agora pode ser executado diretamente (`if __name__ == "__main__":`), servindo como ponto de entrada para a automação.

### 3. Configuração
- O script busca automaticamente a chave em `key-json/mvp-tdah-dialogflow-pytho-q9ys-4e593eb54acb.json`.
- Integração com variáveis de ambiente do `.env` para `GCP_PROJECT_ID`.

## Como Testar
1. Certifique-se de que a chave de serviço válida esteja em `key-json/`.
2. O script gerencia automaticamente o ambiente virtual, mas se precisar instalar dependências manualmente:
   ```bash
   python3 -m venv .venv_stable
   source .venv_stable/bin/activate
   pip install -r requirements.txt
   ```
3. Execute o script de deploy:
   ```bash
   ./scripts/deploy_intents.sh
   ```
4. Verifique o output no terminal e o arquivo `automation_report.log`.
5. Confirme as alterações no Console do Dialogflow.

## Validação
- [x] Script executável e testado localmente (dry-run).
- [x] Variáveis de ambiente configuradas corretamente.
- [x] Lógica de retry verificada.
- [x] Tratamento de credenciais inválidas verificado.
