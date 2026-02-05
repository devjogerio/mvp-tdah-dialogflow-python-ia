# Pull Request: Implementação do Sistema de Versionamento e Release

**Título Sugerido:** `feat: implement version management system and CI/CD automation`

## 📝 Descrição

Este PR implementa um sistema robusto de versionamento semântico (SemVer) e automação de releases para o projeto MVP TDAH. O objetivo é padronizar o ciclo de vida do software, garantindo consistência entre código, tags e documentação, além de reforçar a qualidade via Git Hooks.

### 🔗 Issue Relacionada

Closes # (insira o número da issue se houver)

## 🛠️ Mudanças Realizadas

### 1. Versionamento Semântico

- **Arquivos de Controle**: Adicionados `version.txt`, `package.json` e `CHANGELOG.md` para rastreamento centralizado da versão.
- **Script de Automação**: Criado `ops/version_manager.py` para realizar _bumps_ de versão (patch, minor, major) sincronizados em todos os arquivos.

### 2. Controle de Qualidade (Git Hooks)

- **Pre-commit**: Valida se a versão no `version.txt` coincide com `package.json` antes de permitir o commit.
- **Pre-push**: Executa toda a suíte de testes (`pytest`) antes de enviar para o remoto, prevenindo que código quebrado chegue ao repositório.
- **Instalador**: Script `scripts/install_hooks.sh` para configuração fácil do ambiente de dev.

### 3. CI/CD & Releases

- **GitHub Actions**: Atualizado workflow `ci-cd.yml` para detectar novas tags (`v*`) e criar Releases no GitHub automaticamente, gerando notas de lançamento baseadas no histórico.

## 📸 Demonstração

### Estrutura de Arquivos

```text
├── CHANGELOG.md          # Histórico de mudanças
├── package.json          # Configuração e Scripts
├── version.txt           # Fonte da verdade da versão
├── ops/
│   └── version_manager.py # Script de bump
├── githooks/             # Hooks locais
└── .github/workflows/    # CI/CD atualizado
```

### Exemplo de Uso (Bump de Versão)

```bash
python3 ops/version_manager.py minor
# Output: Atualizando versão: 0.1.0 -> 0.2.0
```

## 🧪 Instruções de Teste

1. **Configuração Inicial**:

   ```bash
   ./scripts/install_hooks.sh
   ```

2. **Teste de Bump de Versão**:
   - Execute: `python3 ops/version_manager.py patch`
   - Verifique se `version.txt` mudou.
   - Verifique se `CHANGELOG.md` tem nova entrada.

3. **Teste de Git Hooks**:
   - Tente alterar `version.txt` manualmente para um valor diferente de `package.json` e tente commitar. O commit deve falhar.
   - Rode `pytest` para garantir que tudo passa.

## ✅ Checklist de Pré-Merge

- [x] O código segue os padrões de estilo do projeto (PEP 8).
- [x] Todos os testes unitários passaram localmente.
- [x] A documentação (CHANGELOG, README) foi atualizada.
- [x] Não há conflitos com a branch `develop`.
- [x] Git Hooks testados e funcionais.
- [x] Script de automação verificado em ambiente dev.

---

**Revisor**: Por favor, valide se os hooks estão executáveis após o clone e se o script Python roda sem erros de dependência.
