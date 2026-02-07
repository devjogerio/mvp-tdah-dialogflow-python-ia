from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import os
import logging
from typing import List

logger = logging.getLogger(__name__)


class OpenSearchService:
    def __init__(self, host: str, region: str = "us-east-1"):
        self.host = host.replace("https://", "").replace("http://", "")
        self.region = region

        # Configuração flexível para ambiente local (Docker) vs AWS
        is_local = os.environ.get("IS_LOCAL", "false").lower() == "true"

        if is_local:
            logger.info("Inicializando OpenSearch em modo LOCAL")
            auth = (os.environ.get("OPENSEARCH_USER", "admin"),
                    os.environ.get("OPENSEARCH_PASSWORD", "admin"))
            port = int(os.environ.get("OPENSEARCH_PORT", 9200))
            use_ssl = os.environ.get(
                "OPENSEARCH_USE_SSL", "false").lower() == "true"
            verify_certs = False
        else:
            credentials = boto3.Session().get_credentials()
            if credentials:
                auth = AWSV4SignerAuth(credentials, region, 'aoss')
            else:
                auth = ('admin', 'admin')  # Fallback

            port = 443
            use_ssl = True
            verify_certs = True

        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': port}],
            http_auth=auth,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
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
