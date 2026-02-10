# Guia de Resolução de Conflitos e Relatório Técnico

## 1. Origem dos Conflitos

Durante a fusão (merge) da branch `origin/develop` na feature branch `feature/multi-llm-support`, foram detectados conflitos em três arquivos principais. Esses conflitos ocorreram devido a alterações concorrentes realizadas em ambas as branches desde o ponto de divergência.

### Arquivos Afetados:

1.  **`README.md`**: Ambas as branches modificaram o conteúdo. A branch `develop` adicionou badges de status e novas seções de automação, enquanto a `feature/multi-llm-support` atualizou a descrição do projeto e adicionou detalhes sobre a nova arquitetura Multi-LLM.
2.  **`src/dialogflow/manager.py`**: Houve divergência na implementação do método `create_entity_type`. A branch `develop` continha uma versão mais robusta com lógica de retry e validação aprimorada, enquanto a feature branch possuía uma versão com lógica simplificada.
3.  **`src/core/bedrock_integration.py`**: Este arquivo foi deletado na `feature/multi-llm-support` (devido à refatoração para arquitetura modular) mas foi modificado na `develop` (provavelmente correções ou melhorias pontuais).

## 2. Estratégia de Resolução

Adotamos uma abordagem sistemática para garantir a integridade do código e a preservação das funcionalidades mais recentes:

1.  **`src/core/bedrock_integration.py`**:
    - **Decisão**: Manter a deleção.
    - **Justificativa**: A arquitetura foi refatorada para usar `src/core/assistant_service.py` e o padrão Factory em `src/core/llm/`, tornando o arquivo antigo obsoleto.

2.  **`src/dialogflow/manager.py`**:
    - **Decisão**: Aceitar as alterações da `origin/develop`.
    - **Justificativa**: A versão da `develop` continha melhorias críticas de robustez (retry policy, logs detalhados) que são essenciais para a automação em produção.

3.  **`README.md`**:
    - **Decisão**: Fusão manual (Merge).
    - **Justificativa**: Combinamos as badges e seções de automação da `develop` com as novas descrições de arquitetura IA da feature branch, garantindo uma documentação completa.

## 3. Guia Passo-a-Passo de Resolução

Abaixo estão os comandos utilizados para diagnosticar e resolver os conflitos:

### Passo 1: Diagnóstico

```bash
# Verificar status e branches
git status
git branch -a

# Tentar o merge (que resulta em conflito)
git merge origin/develop
```

### Passo 2: Resolução Manual

#### Para arquivos deletados vs modificados:

```bash
# Confirmar a deleção do arquivo obsoleto
git rm src/core/bedrock_integration.py
```

#### Para conflitos de conteúdo (edição manual):

Edite os arquivos marcados (ex: `README.md`, `src/dialogflow/manager.py`) procurando por:

```text
<<<<<<< HEAD
(Conteúdo da sua branch)
=======
(Conteúdo da branch develop)
>>>>>>> origin/develop
```

Escolha o bloco correto ou combine-os, removendo os marcadores.

### Passo 3: Validação

Antes de commitar, execute os testes para garantir que a resolução não quebrou nada.

```bash
# Instalar dependências atualizadas (caso requirements.txt tenha mudado)
pip install -r requirements.txt

# Rodar testes
pytest tests/
```

### Passo 4: Commit e Push

```bash
# Adicionar arquivos resolvidos
git add README.md src/dialogflow/manager.py requirements.txt

# Commitar a resolução
git commit -m "fix: resolve merge conflicts in README, manager.py and requirements"

# Enviar para o remoto
git push origin feature/multi-llm-support
```

## 4. Práticas Preventivas

Para minimizar conflitos futuros, recomendamos:

1.  **Sincronização Frequente**: Execute `git pull origin develop` (ou rebase) na sua feature branch diariamente para resolver conflitos pequenos antes que se tornem grandes.
2.  **Commits Atômicos**: Mantenha commits focados em uma única responsabilidade. Isso facilita a identificação e resolução de conflitos específicos.
3.  **Comunicação**: Alinhe com o time quando refatorações estruturais (como deletar arquivos core) forem planejadas.
4.  **Feature Flags**: Use feature flags para integrar código incompleto na `develop` sem quebrar a produção, evitando branches de longa duração.

## 5. Validação Final

Os testes automatizados foram executados com sucesso após a resolução:

- **Status**: ✅ Passou (25 testes)
- **Ambiente**: Python 3.9.6 (Estável)
- **Verificação**: A integridade da nova arquitetura Multi-LLM foi mantida e as melhorias de automação da `develop` foram preservadas.
