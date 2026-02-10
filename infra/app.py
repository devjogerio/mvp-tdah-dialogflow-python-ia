#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks.chatbot_stack import ChatbotStack

app = cdk.App()

# Definindo ambiente (pode ser parametrizado via env vars)
env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
)

ChatbotStack(app, "TdahChatbotStack", env=env)

app.synth()
