#!/bin/bash
# Script para configurar Git Hooks do projeto

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"

echo "Configurando Git Hooks em $HOOKS_DIR..."

# Cria o arquivo pre-commit se não existir
if [ ! -f "$PRE_COMMIT_HOOK" ]; then
    echo "#!/bin/bash" > "$PRE_COMMIT_HOOK"
    echo "echo '🔍 Executando organização automática de documentação...'" >> "$PRE_COMMIT_HOOK"
    echo "python3 \"$PROJECT_ROOT/scripts/organize_docs.py\"" >> "$PRE_COMMIT_HOOK"
    echo "# Se o script moveu arquivos que estavam sendo commitados, o git pode reclamar." >> "$PRE_COMMIT_HOOK"
    echo "# Mas como o objetivo é ignorar esses arquivos, isso é o esperado." >> "$PRE_COMMIT_HOOK"
    echo "exit 0" >> "$PRE_COMMIT_HOOK"
    
    chmod +x "$PRE_COMMIT_HOOK"
    echo "✅ Hook pre-commit criado com sucesso!"
else
    echo "⚠️  Hook pre-commit já existe. Adicionando chamada se não houver."
    if ! grep -q "organize_docs.py" "$PRE_COMMIT_HOOK"; then
        echo "" >> "$PRE_COMMIT_HOOK"
        echo "python3 \"$PROJECT_ROOT/scripts/organize_docs.py\"" >> "$PRE_COMMIT_HOOK"
        echo "✅ Chamada adicionada ao hook existente."
    else
        echo "ℹ️  Hook já configurado."
    fi
fi
