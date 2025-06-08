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

resource "null_resource" "get_vibes_build" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/lambda_bundles/get_vibes_lambda
      mkdir -p ${path.module}/lambda_bundles/get_vibes_lambda
      cp -r ../../../backend-new/lambdas/get-vibes/*.py ${path.module}/lambda_bundles/get_vibes_lambda/

      if [ -f ../../../backend-new/lambdas/get-vibes/requirements.txt ]; then
        pip install -r ../../../backend-new/lambdas/get-vibes/requirements.txt -t ${path.module}/lambda_bundles/get_vibes_lambda
      fi
    EOT
  }

  triggers = {
    # Trigger if any Python files changed
    python_files_hash = join("", [for file in fileset("../../../backend-new/lambdas/get-vibes", "*.py") :
      filesha1("../../../backend-new/lambdas/get-vibes/${file}")]
    )

    # Trigger if requirements.txt changed
    requirements_hash = filesha1("../../../backend-new/lambdas/get-vibes/requirements.txt")
  }
}

data "archive_file" "get_vibes_lambda" {
  depends_on  = [null_resource.get_vibes_build]
  type        = "zip"
  source_dir  = "${path.module}/lambda_bundles/get_vibes_lambda"
  output_path = "${path.module}/lambda_zips/get_vibes_lambda.zip"
}

resource "aws_lambda_function" "get_vibes_lambda" {
  function_name    = "get-vibes"
  filename         = data.archive_file.get_vibes_lambda.output_path
  source_code_hash = data.archive_file.get_vibes_lambda.output_base64sha256
  handler          = "handler.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec.arn
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
