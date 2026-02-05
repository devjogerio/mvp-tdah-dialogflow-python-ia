resource "aws_opensearchserverless_security_policy" "encryption" {
  name        = "encryption-policy"
  type        = "encryption"
  description = "Encryption policy for TDAH collection"
  policy = jsonencode({
    Rules = [
      {
        ResourceType = "collection"
        Resource = [
          "collection/${var.collection_name}"
        ]
      }
    ],
    AWSOwnedKey = true
  })
}

resource "aws_opensearchserverless_collection" "kb_collection" {
  name = var.collection_name
  type = "VECTORSEARCH"
  depends_on = [aws_opensearchserverless_security_policy.encryption]
}

output "collection_endpoint" {
  value = aws_opensearchserverless_collection.kb_collection.collection_endpoint
}
