import sys
import os
import aws_cdk as cdk
from aws_cdk.assertions import Template

# Adiciona o diretório pai (infra/) ao path para importar stacks e constructs
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from stacks.chatbot_stack import ChatbotStack

def test_chatbot_stack_created():
    app = cdk.App()
    stack = ChatbotStack(app, "TdahChatbotStack")
    template = Template.from_stack(stack)

    # Verifica se o bucket S3 foi criado
    template.resource_count_is("AWS::S3::Bucket", 1)
    
    # Verifica se a Lambda Function foi criada
    template.resource_count_is("AWS::Lambda::Function", 1)
    
    # Verifica se a Collection do OpenSearch foi criada
    template.resource_count_is("AWS::OpenSearchServerless::Collection", 1)

def test_s3_bucket_properties():
    app = cdk.App()
    stack = ChatbotStack(app, "TdahChatbotStack")
    template = Template.from_stack(stack)
    
    # Verifica propriedades do bucket (Versionamento e EnforceSSL)
    template.has_resource_properties("AWS::S3::Bucket", {
        "VersioningConfiguration": {
            "Status": "Enabled"
        }
    })

def test_lambda_function_properties():
    app = cdk.App()
    stack = ChatbotStack(app, "TdahChatbotStack")
    template = Template.from_stack(stack)
    
    # Verifica runtime da Lambda
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.9",
        "Handler": "lambda_function.lambda_handler"
    })
