# Pull Request: Automação de Deploy do Dialogflow e Organização de Documentação

## Resumo

Este PR introduz melhorias significativas na infraestrutura do projeto, abrangendo duas áreas principais:

1. **Automação de Deploy do Dialogflow**: Scripts robustos para sincronização de intents/entidades.
2. **Organização de Documentação**: Automação para padronizar a localização de arquivos de documentação e limpar o versionamento.

## Alterações Principais

### 1. Automação de Documentação (Novo)

- **Script Organizador (`scripts/organize_docs.py`)**: Move automaticamente arquivos `.md` soltos para a pasta `docs/`, mantendo a raiz limpa.
- **Git Hooks (`scripts/setup_hooks.sh`)**: Instala um hook `pre-commit` que executa a organização automaticamente antes de cada commit.
- **Regras de Versionamento (`.gitignore`)**:
  - Ignora todo o conteúdo de `docs/` por padrão para evitar poluição no repositório.
  - Mantém exceções explícitas para arquivos críticos: `CHANGELOG.md` e `MIGRATION.md`.
  - Remove arquivos de documentação técnica/temporária do controle de versão.

### 2. Script de Automação Dialogflow (`scripts/deploy_intents.sh`)

- **Configuração de Ambiente**: Define automaticamente `GOOGLE_APPLICATION_CREDENTIALS` e `PYTHONPATH`.
- **Compatibilidade**: Exporta `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` para mitigar problemas com Python 3.x recentes.
- **Resiliência**: Implementa lógica de retry (3 tentativas) com backoff exponencial no nível do shell.
- **Validação**: Verifica a existência do arquivo de chave JSON e do script Python antes da execução.
- **Logging**: Fornece logs coloridos e detalhados de cada etapa.

### 3. Melhorias no Gerenciador (`src/dialogflow/manager.py`)

- **Tratamento de Erros**: Adicionado bloco `try-except` específico para `DefaultCredentialsError` e `ValueError` na inicialização.
- **Modo Standalone**: O módulo agora pode ser executado diretamente como ponto de entrada para a automação.

## Como Testar

### Teste da Automação de Documentação

1. Crie um arquivo `.md` temporário na raiz ou em qualquer subpasta (ex: `teste_temp.md`).
2. Tente fazer um commit.
3. Verifique se o arquivo foi movido automaticamente para `docs/` e se o commit prosseguiu (ou se o git avisou sobre a mudança).
4. Verifique se `git status` mostra o arquivo em `docs/` como untracked/ignored (se não for uma das exceções).

### Teste do Deploy Dialogflow

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

## Validação

- [x] Script de organização de docs testado e funcional.
- [x] `.gitignore` atualizado e validado (arquivos antigos removidos do cache).
- [x] Script de deploy executável e testado localmente.
- [x] Variáveis de ambiente configuradas corretamente.
- [x] Lógica de retry verificada.
