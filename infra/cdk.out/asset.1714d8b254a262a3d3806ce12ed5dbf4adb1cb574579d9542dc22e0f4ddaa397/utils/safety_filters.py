import re
from typing import Tuple, Optional

"""
Módulo de filtros de segurança para o Chatbot de Saúde Mental.
Responsável por identificar intenções de risco (RF02).
"""

# Lista de palavras-chave e padrões de risco (Exemplo simplificado)
# Em produção, isso deve ser mais robusto ou usar um modelo classificador.
RISK_KEYWORDS = [
    r"\bsuic[ií]d",
    r"\bmorrer",
    r"\bmatar",
    r"\bacabar com tudo",
    r"\bautomutila",
    r"\bcortar os pulsos",
    r"\bdesaparecer",
    r"\bnão aguento mais viver"
]

EMERGENCY_MESSAGE = (
    "Sinto muito que você esteja se sentindo assim. "
    "Por favor, saiba que você não está sozinho. "
    "Se estiver em perigo imediato ou pensando em se machucar, "
    "ligue para o **CVV (Centro de Valorização da Vida)** no número **188** "
    "ou procure o serviço de emergência mais próximo."
)

def check_safety(text: str) -> Tuple[bool, Optional[str]]:
    """
    Verifica se o texto contém conteúdo de risco.

    Args:
        text (str): O texto de entrada do usuário.

    Returns:
        Tuple[bool, Optional[str]]: 
            - bool: True se for seguro, False se for detectado risco.
            - str: Mensagem de emergência se risco detectado, None caso contrário.
    """
    if not text:
        return True, None

    normalized_text = text.lower()
    
    for pattern in RISK_KEYWORDS:
        if re.search(pattern, normalized_text):
            return False, EMERGENCY_MESSAGE
            
    return True, None
