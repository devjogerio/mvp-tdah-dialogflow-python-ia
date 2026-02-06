from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct

class ComputeConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, lambda_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Role da Lambda
        lambda_role = iam.Role(
            self, "ChatbotLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=f"{lambda_name}-role"
        )
        
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        # Função Lambda
        # Nota: O código aponta para src/ mas em deploy real usaria-se DockerImageFunction ou zip
        # Para MVP/Migração, usamos um inline ou asset
        self.function = _lambda.Function(
            self, "ChatbotLambda",
            function_name=lambda_name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("../src"), # Aponta para pasta src na raiz
            role=lambda_role,
            environment={
                "LOG_LEVEL": "INFO"
            }
        )

        CfnOutput(self, "LambdaArn", value=self.function.function_arn)
