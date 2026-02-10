# Auto-Understanding System

## 🌟 Visão Geral
Este sistema automatizado permite que o chatbot "aprenda" a partir de documentos de estudo de caso em Markdown. Ele analisa o texto, extrai padrões de conversação e atualiza automaticamente a configuração do Dialogflow.

## 🏗️ Arquitetura

### Componentes
1.  **Markdown Parser (`markdown_parser.py`)**:
    *   Lê arquivos Markdown estruturados.
    *   Identifica cabeçalhos como *Intents*.
    *   Extrai conteúdo como *Responses*.
    *   Mapeia palavras-chave para *Training Phrases* usando heurísticas pré-definidas.
    *   Identifica entidades (Especialistas, Sintomas, Tratamentos).

2.  **Migration Script (`migrate_case_study.py`)**:
    *   Carrega a configuração existente (`initial_config.json`).
    *   Executa o parser no arquivo fonte.
    *   Realiza um *Merge Inteligente* (Upsert):
        *   Intents existentes são atualizadas.
        *   Novas Intents são criadas.
        *   Entidades são enriquecidas com novos valores.
    *   Valida o schema JSON antes de salvar.

## 🚀 Como Usar

### Pré-requisitos
*   Python 3.8+
*   Arquivo de estudo de caso formatado em Markdown (ex: `esudo-de-caso.md`).

### Execução
Para rodar a migração e atualizar o conhecimento do bot:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 src/dialogflow/scripts/migrate_case_study.py
```

## 🧪 Testes
O sistema possui testes unitários para garantir a integridade do parser:

```bash
python3 -m unittest tests/test_markdown_parser.py
```

## 📝 Padrões de Arquivo Markdown
O parser espera a seguinte estrutura:

```markdown
## Título do Tópico (Vira Intent)
- Conteúdo em bullets (Vira Resposta do Bot)
- Mais conteúdo...
```

## 🔄 Fluxo de CI/CD
1.  Desenvolvedor atualiza o arquivo Markdown.
2.  Script de validação checa integridade.
3.  Pipeline executa a migração.
4.  Arquivo `initial_config.json` é commitado com novas definições.
