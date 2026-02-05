resource "aws_iam_role" "lambda_role" {
  name = "${var.lambda_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Em um cenário real, adicionaríamos permissões para Bedrock e OpenSearch aqui

resource "aws_lambda_function" "chatbot_lambda" {
  filename      = "lambda_function_payload.zip" # Placeholder
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "src.lambda_function.lambda_handler"
  runtime       = "python3.9"
  
  # Placeholder para o código
  # Na automação real, o código seria zipado e enviado
}
