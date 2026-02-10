import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class CaseStudyParser:
    """
    Parser especializado em extrair estruturas de conversação (Intents e Entities)
    a partir de arquivos Markdown estruturados como estudos de caso.
    """

    def __init__(self):
        # Mapeamento heurístico de tópicos para frases de treinamento
        self.topic_triggers = {
            "Acolhimento e Suspeita": [
                "Como funciona o acolhimento?",
                "Tenho suspeita de TDAH",
                "Estou desanimado e sem foco",
                "Onde devo ir primeiro?",
                "Sintomas iniciais de TDAH",
            ],
            "Avaliação Diagnóstica": [
                "Como é feito o diagnóstico?",
                "Preciso de um psiquiatra ou neurologista?",
                "O que acontece na avaliação?",
                "Diferença entre TDAH e depressão",
                "Quais exames preciso fazer?",
            ],
            "Planejamento do Tratamento": [
                "Qual o tratamento para TDAH?",
                "Preciso tomar remédio?",
                "Como tratar TDAH e depressão juntos?",
                "O que é abordagem multimodal?",
                "Tratamento medicamentoso",
            ],
            "Intervenções Terapêuticas": [
                "Tratamento sem remédio",
                "O que é TCC?",
                "Dicas de organização",
                "Mudanças no estilo de vida",
                "Psicoeducação para TDAH",
            ],
            "Acompanhamento Contínuo": [
                "Preciso voltar no médico?",
                "Como saber se o tratamento está funcionando?",
                "Acompanhamento a longo prazo",
                "Ajuste de medicação",
            ],
            "Atendimento (SUS)": [
                "O SUS trata TDAH?",
                "Como conseguir remédio no SUS?",
                "Psicólogo pelo SUS",
                "Atendimento gratuito para TDAH",
            ],
        }

        self.entities_map = {
            "Especialista": [
                "Psiquiatra",
                "Neurologista",
                "Clínico Geral",
                "Psicólogo",
            ],
            "Sintoma": [
                "desânimo",
                "falta de motivação",
                "baixa autoestima",
                "esquecimentos",
                "desorganização",
            ],
            "Tratamento": [
                "Antidepressivos",
                "Estimulantes",
                "TCC",
                "Terapia Cognitivo-Comportamental",
                "Psicoeducação",
            ],
        }

    def parse(self, file_path: str) -> Dict[str, List[Dict]]:
        """
        Lê o arquivo Markdown e retorna um dicionário com intents e entities.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        intents = self._extract_intents(content)
        entities = self._extract_entities(content)

        return {"intents": intents, "entities": entities}

    def _extract_intents(self, content: str) -> List[Dict]:
        intents = []
        # Divide por cabeçalhos de nível 2 (##)
        sections = re.split(r"^##\s+", content, flags=re.MULTILINE)

        for section in sections:
            if not section.strip() or section.startswith("# Estudo"):
                continue

            lines = section.strip().split("\n")
            title_line = lines[0].strip()

            # Limpa o título (remove numeração "1. ", "2. ")
            clean_title = re.sub(r"^\d+\.\s+", "", title_line)
            # Remove parenteses ex: (Atenção Primária)
            clean_title = re.sub(r"\s*\(.*\)", "", clean_title).strip()

            # Identifica chave de trigger
            triggers = []
            for key, phrases in self.topic_triggers.items():
                if (
                    key.lower() in title_line.lower()
                    or clean_title.lower() in key.lower()
                ):
                    triggers = phrases
                    break

            if not triggers:
                triggers = [
                    f"Falar sobre {clean_title}",
                    f"Dúvidas sobre {clean_title}",
                ]

            # Constrói a resposta a partir do conteúdo
            response_text = []
            for line in lines[1:]:
                if line.strip().startswith("-") or line.strip().startswith("*"):
                    response_text.append(line.strip())

            # Se não achou bullets, pega parágrafos
            if not response_text:
                para = []
                for line in lines[1:]:
                    if line.strip():
                        para.append(line.strip())
                if para:
                    response_text = para[:3]  # Limita a 3 parágrafos

            if response_text:
                full_response = "\n".join(response_text)

                intent = {
                    "display_name": f"CaseStudy - {clean_title}",
                    "training_phrases": triggers,
                    "messages": [{"text": [full_response]}],
                    "priority": 500000,
                }
                intents.append(intent)

        return intents

    def _extract_entities(self, content: str) -> List[Dict]:
        extracted_entities = []

        # Lógica simplificada: Verifica se as palavras-chave pré-definidas aparecem no texto
        # Em um sistema real, usaria NLP (spacy/nltk) para extração

        for entity_name, values in self.entities_map.items():
            found_entries = []
            for val in values:
                if val.lower() in content.lower():
                    found_entries.append({"value": val.lower(), "synonyms": [val]})

            if found_entries:
                extracted_entities.append(
                    {
                        "display_name": entity_name,
                        "kind": "KIND_MAP",
                        "entries": found_entries,
                    }
                )

        return extracted_entities
