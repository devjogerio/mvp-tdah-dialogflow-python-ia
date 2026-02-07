import os
import sys
from pathlib import Path

# Configuração de caminhos permitidos e ignorados
ALLOWED_DIRS = [
    "docs",
    ".github",
    "venv",
    ".venv",
    "node_modules",
    ".pytest_cache",
    "__pycache__"
]

ALLOWED_FILES = [
    "README.md"
]

IGNORE_DIRS = [
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "cdk.out"
]

def is_allowed(file_path: Path, root_path: Path) -> bool:
    # Caminho relativo à raiz do projeto
    try:
        rel_path = file_path.relative_to(root_path)
    except ValueError:
        return False

    # Verifica se é um arquivo permitido na raiz
    if str(rel_path) in ALLOWED_FILES:
        return True

    # Verifica se está em um diretório permitido
    first_part = rel_path.parts[0]
    if first_part in ALLOWED_DIRS:
        return True
        
    # Verifica subdiretórios ignorados explicitamente (como infra/.pytest_cache)
    # Se qualquer parte do caminho estiver em ALLOWED_DIRS (ex: infra/venv/...), permitimos?
    # Melhor: verificar se o prefixo bate com ALLOWED_DIRS ou se é um diretório de build/cache comum
    
    # Lógica refinada:
    # 1. Se estiver na raiz, deve estar em ALLOWED_FILES.
    # 2. Se estiver em subpasta, a primeira pasta deve ser 'docs' OU ser uma pasta ignorada de sistema/build.
    
    if len(rel_path.parts) > 1:
        # Permite arquivos .md dentro de infra/ se estiverem em pastas ignoradas?
        # O requisito do usuário é: "toda a documentação futura seja ... em docs"
        # Arquivos de licença em venv/node_modules são ok.
        
        # Verifica se qualquer parte do caminho está em ALLOWED_DIRS (para pegar venv aninhado, etc)
        for part in rel_path.parts:
             if part in ALLOWED_DIRS or part in IGNORE_DIRS:
                 return True
                 
    return False

def main():
    root_path = Path(os.getcwd())
    print(f"🔍 Verificando localização de arquivos .md em: {root_path}")
    
    violations = []
    
    for path in root_path.rglob("*.md"):
        # Ignora diretórios ocultos do sistema se não estiverem na lista explícita, mas rglob já pega tudo
        # Vamos filtrar na função is_allowed
        
        if not is_allowed(path, root_path):
            violations.append(str(path.relative_to(root_path)))

    if violations:
        print("\n❌ Erro: Arquivos de documentação encontrados fora de 'docs/'.")
        print("Por favor, mova os seguintes arquivos para a pasta 'docs/':")
        for v in violations:
            print(f" - {v}")
        print("\nExceções permitidas: README.md, .github/, venv/, node_modules/")
        sys.exit(1)
    
    print("✅ Todos os arquivos .md estão nos locais corretos.")
    sys.exit(0)

if __name__ == "__main__":
    main()
