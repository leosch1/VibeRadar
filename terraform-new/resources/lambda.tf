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

resource "aws_iam_role_policy" "dynamodb" {
  name = "lambda-dynamodb-access"
  role = module.lambda_get_vibes.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Scan",
        "dynamodb:Query"
      ],
      Resource = aws_dynamodb_table.vibes.arn
    }]
  })
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
