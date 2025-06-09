resource "aws_api_gateway_rest_api" "this" {
  name        = "viberadar-api"
  description = "API Gateway v1 for VibeRadar"
}

data "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  path        = "/"
}

resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_method.get_vibes,
      aws_api_gateway_integration.get_vibes_integration,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "default" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  deployment_id = aws_api_gateway_deployment.this.id
  stage_name    = "default"
}

### Endpoint for /getVibes ###

resource "aws_api_gateway_resource" "get_vibes" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "getVibes"
}

resource "aws_api_gateway_method" "get_vibes" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.get_vibes.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_vibes_integration" {
  rest_api_id             = aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.get_vibes.id
  http_method             = aws_api_gateway_method.get_vibes.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.lambda_get_vibes.lambda_function_invoke_arn
}

### Endpoint for /getOtherConnections ###

# TODO
