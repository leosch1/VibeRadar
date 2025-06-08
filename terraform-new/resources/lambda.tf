resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy_attachment" "lambda_logs" {
  name       = "lambda_logs"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

### Lambda Function for /getVibes ###

data "archive_file" "get_vibes_lambda" {
  type        = "zip"
  source_dir  = "../../../backend-new/lambdas/get-vibes"
  output_path = "${path.module}/lambda_zips/get_vibes_lambda.zip"
}

resource "aws_lambda_function" "get_vibes_lambda" {
  function_name = "get-vibes"
  filename      = data.archive_file.get_vibes_lambda.output_path
  source_code_hash = data.archive_file.get_vibes_lambda.output_base64sha256
  handler       = "handler.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec.arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_vibes_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.this.execution_arn}/*/POST/getVibes"
}

### Lambda Function for /getOtherConnections ###

# TODO
