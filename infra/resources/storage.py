from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class StorageConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self, "KnowledgeBaseBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.RETAIN, # Prevenir deleção acidental de dados
            enforce_ssl=True
        )

        CfnOutput(self, "BucketArn", value=self.bucket.bucket_arn)
        CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
