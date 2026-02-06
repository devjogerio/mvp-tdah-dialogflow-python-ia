from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class OpenSearchService:
    def __init__(self, host: str, region: str = "us-east-1"):
        self.host = host.replace("https://", "")
        self.region = region
        
        credentials = boto3.Session().get_credentials()
        # Fallback seguro para mock/testes sem credenciais
        if credentials:
            auth = AWSV4SignerAuth(credentials, region, 'aoss')
        else:
            auth = ('admin', 'admin') # Mock apenas para testes locais fora da AWS

        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            pool_maxsize=20
        )
        self.index_name = "tdah-knowledge-index"

    def search(self, query_vector: List[float], k: int = 3) -> str:
        """
        Realiza busca vetorial no OpenSearch.
        """
        try:
            body = {
                "size": k,
                "query": {
                    "knn": {
                        "embedding_vector": {
                            "vector": query_vector,
                            "k": k
                        }
                    }
                }
            }
            
            response = self.client.search(
                body=body,
                index=self.index_name
            )
            
            hits = response['hits']['hits']
            context = "\n".join([hit['_source']['text'] for hit in hits])
            return context
            
        except Exception as e:
            logger.error(f"Erro na busca OpenSearch: {str(e)}")
            return ""

    def index_document(self, doc_id: str, text: str, vector: List[float]):
        """
        Indexa um documento (usado para popular a base).
        """
        body = {
            "text": text,
            "embedding_vector": vector
        }
        self.client.index(index=self.index_name, id=doc_id, body=body)
