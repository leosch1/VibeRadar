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

module "lambda_get_vibes" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 6.0"

  function_name = "get-vibes"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  source_path   = "../../../backend-new/lambdas/get-vibes"

  create_role                   = true
  attach_cloudwatch_logs_policy = true
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_get_vibes.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.this.execution_arn}/*/POST/getVibes"
}

### Lambda Function for /getOtherConnections ###

# TODO
