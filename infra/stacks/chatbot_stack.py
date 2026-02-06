from aws_cdk import (
    Stack,
)
from constructs import Construct
from .constructs.storage import StorageConstruct
from .constructs.search import SearchConstruct
from .constructs.compute import ComputeConstruct

class ChatbotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Variáveis (podem vir de context ou env vars)
        # Usando os defaults do Terraform antigo para manter consistência
        bucket_name = "mvp-tdah-kb-docs"
        collection_name = "tdah-knowledge"
        lambda_name = "tdah-chatbot-handler"

        # Storage
        self.storage = StorageConstruct(self, "Storage", bucket_name=bucket_name)

        # Search
        self.search = SearchConstruct(self, "Search", collection_name=collection_name)

        # Compute
        self.compute = ComputeConstruct(self, "Compute", lambda_name=lambda_name)
