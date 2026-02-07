#!/usr/bin/env python3
import os
import shutil
import logging

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("DocsOrganizer")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# Arquivos e pastas a ignorar
IGNORED_DIRS = {
    ".git", ".venv", ".venv_stable", "venv", "env", 
    "node_modules", "docs", "__pycache__", ".idea", ".vscode"
}
IGNORED_FILES = {
    "README.md", "PR_DESCRIPTION.md", "PULL_REQUEST_TEMPLATE.md"
}

def is_ignored(path):
    """Verifica se o caminho deve ser ignorado."""
    parts = path.split(os.sep)
    for part in parts:
        if part in IGNORED_DIRS:
            return True
    return False

def organize_docs():
    """Move arquivos .md soltos para a pasta docs/."""
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        logger.info(f"Pasta criada: {DOCS_DIR}")

    moved_count = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Modifica dirs in-place para pular pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith(".md") and file not in IGNORED_FILES:
                source_path = os.path.join(root, file)
                
                # Se o arquivo já está em docs/, pula (garantido pelo IGNORED_DIRS, mas reforçando)
                if DOCS_DIR in os.path.abspath(source_path):
                    continue

                # Define destino
                dest_path = os.path.join(DOCS_DIR, file)
                
                # Evita sobrescrever se já existe (renomeia se necessário)
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(DOCS_DIR, f"{base}_{counter}{ext}")
                        counter += 1

                try:
                    shutil.move(source_path, dest_path)
                    logger.info(f"♻️  Movido: {source_path} -> {dest_path}")
                    moved_count += 1
                except Exception as e:
                    logger.error(f"❌ Erro ao mover {source_path}: {e}")

    if moved_count > 0:
        logger.info(f"✅ Organização concluída! {moved_count} arquivos movidos para docs/.")
    else:
        logger.info("✅ Nenhum arquivo .md solto encontrado.")

if __name__ == "__main__":
    organize_docs()
