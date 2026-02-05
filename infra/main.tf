terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

module "storage" {
  source = "./modules/storage"
  bucket_name = var.bucket_name
}

module "search" {
  source = "./modules/search"
  collection_name = var.collection_name
}

module "compute" {
  source = "./modules/compute"
  lambda_name = var.lambda_name
  s3_bucket_arn = module.storage.bucket_arn
  opensearch_endpoint = module.search.collection_endpoint
}
