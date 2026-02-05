#!/usr/bin/env python3
import sys
import json
import re
import os
from datetime import datetime

"""
Script de Gerenciamento de Versão (Semantic Versioning).
Responsável por atualizar version.txt, package.json e CHANGELOG.md.
"""

FILES = {
    "txt": "version.txt",
    "json": "package.json",
    "changelog": "CHANGELOG.md"
}

def get_current_version():
    try:
        with open(FILES["txt"], "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def bump_version(current_version, part):
    major, minor, patch = map(int, current_version.split('.'))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print("Parte inválida. Use: major, minor, ou patch.")
        sys.exit(1)
    return f"{major}.{minor}.{patch}"

def update_files(new_version):
    # Update version.txt
    with open(FILES["txt"], "w") as f:
        f.write(new_version)
    
    # Update package.json
    try:
        with open(FILES["json"], "r") as f:
            data = json.load(f)
        data["version"] = new_version
        with open(FILES["json"], "w") as f:
            json.dump(data, f, indent=2)
            f.write('\n') # Add newline at end of file
    except FileNotFoundError:
        pass

    # Update CHANGELOG.md
    update_changelog(new_version)

def update_changelog(new_version):
    date_str = datetime.now().strftime("%Y-%m-%d")
    header_pattern = r"## \[Unreleased\]"
    new_header = f"## [Unreleased]\n\n### Added\n- \n\n### Changed\n- \n\n### Deprecated\n- \n\n### Removed\n- \n\n### Fixed\n- \n\n### Security\n- \n\n## [{new_version}] - {date_str}"
    
    try:
        with open(FILES["changelog"], "r") as f:
            content = f.read()
        
        if re.search(header_pattern, content):
            new_content = re.sub(header_pattern, new_header, content)
            with open(FILES["changelog"], "w") as f:
                f.write(new_content)
        else:
            print("Cabeçalho [Unreleased] não encontrado no CHANGELOG.md")
    except FileNotFoundError:
        pass

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 ops/version_manager.py [major|minor|patch]")
        sys.exit(1)
    
    part = sys.argv[1]
    current_version = get_current_version()
    new_version = bump_version(current_version, part)
    
    print(f"Atualizando versão: {current_version} -> {new_version}")
    update_files(new_version)
    print("Arquivos atualizados com sucesso.")

if __name__ == "__main__":
    main()
