import unittest
import os
from src.dialogflow.parsers.markdown_parser import CaseStudyParser

class TestCaseStudyParser(unittest.TestCase):
    def setUp(self):
        self.parser = CaseStudyParser()
        self.test_file = "test_case_study.md"
        with open(self.test_file, "w") as f:
            f.write("# Estudo de Caso\n\n## 1. Acolhimento e Suspeita\n\n- **Onde**: UBS.\n- **Ação**: Triagem.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_intents(self):
        result = self.parser.parse(self.test_file)
        self.assertIn("intents", result)
        self.assertTrue(len(result["intents"]) > 0)
        
        intent = result["intents"][0]
        self.assertIn("Acolhimento", intent["display_name"])
        self.assertIn("- **Onde**: UBS.", intent["messages"][0]["text"][0])
        self.assertIn("Tenho suspeita de TDAH", intent["training_phrases"])

    def test_parse_entities(self):
        # Escreve um arquivo com entidades conhecidas
        with open(self.test_file, "w") as f:
            f.write("O paciente deve procurar um Psiquiatra e tomar Antidepressivos.")
            
        result = self.parser.parse(self.test_file)
        self.assertIn("entities", result)
        
        entity_names = [e["display_name"] for e in result["entities"]]
        self.assertIn("Especialista", entity_names)
        self.assertIn("Tratamento", entity_names)

if __name__ == '__main__':
    unittest.main()
