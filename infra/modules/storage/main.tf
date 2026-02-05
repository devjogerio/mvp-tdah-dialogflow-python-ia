resource "aws_s3_bucket" "kb_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.kb_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_arn" {
  value = aws_s3_bucket.kb_bucket.arn
}
