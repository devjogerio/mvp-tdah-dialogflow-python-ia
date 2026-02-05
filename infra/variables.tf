variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 Bucket for Knowledge Base"
  type        = string
  default     = "mvp-tdah-kb-docs"
}

variable "collection_name" {
  description = "OpenSearch Serverless Collection Name"
  type        = string
  default     = "tdah-knowledge"
}

variable "lambda_name" {
  description = "Lambda Function Name"
  type        = string
  default     = "tdah-chatbot-handler"
}
