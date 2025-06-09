# New Terraform Structure for VibeRadar

## Local Development

Make sure you have the following installed:

- Localstack (for local AWS services)
- Docker (for running Localstack)
- Terraform

Start Localstack to simulate AWS services locally by running:

```bash
localstack start
```

Go to the `terraform-new/environments/local` directory and deploy the infrastructure:

```bash
cd terraform-new/environments/local
terraform init
terraform apply
```

This will set up the necessary AWS services locally, including API Gateway, Lambda, and DynamoDB.

The URL for the API Gateway will be printed in the output. You can use this URL to test your Lambda functions locally:

```bash
curl -X POST http://localhost:4566/restapis/<API_GATEWAY_ID>/default/_user_request_/getVibes \
  -H "Content-Type: application/json" \
  -d '{"someData": "blabla"}'
```

## AWS Deployment

The contents of the `terraform-new` get automatically deployed to AWS via GitHub Actions when changes are pushed to the main branch.

To deploy to AWS manually, go to the `terraform-new/environments/aws` directory and run:

```bash
cd terraform-new/environments/aws
terraform init
terraform apply
```
