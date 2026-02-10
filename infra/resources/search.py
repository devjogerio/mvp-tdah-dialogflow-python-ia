import json

from aws_cdk import CfnOutput
from aws_cdk import aws_opensearchserverless as oss
from constructs import Construct


class SearchConstruct(Construct):
    def __init__(
        self, scope: Construct, construct_id: str, collection_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Policy de Criptografia
        encryption_policy = oss.CfnSecurityPolicy(
            self,
            "EncryptionPolicy",
            name=f"{collection_name}-encryption",
            type="encryption",
            policy=json.dumps(
                {
                    "Rules": [
                        {
                            "ResourceType": "collection",
                            "Resource": [f"collection/{collection_name}"],
                        }
                    ],
                    "AWSOwnedKey": True,
                }
            ),
        )

        # Coleção OpenSearch Serverless
        self.collection = oss.CfnCollection(
            self,
            "KbCollection",
            name=collection_name,
            type="VECTORSEARCH",
            description="Colecao de busca vetorial para chatbot TDAH",
        )

        # Dependência explícita para garantir ordem de criação
        self.collection.add_dependency(encryption_policy)

        CfnOutput(
            self, "CollectionEndpoint", value=self.collection.attr_collection_endpoint
        )
        CfnOutput(self, "CollectionId", value=self.collection.attr_id)
