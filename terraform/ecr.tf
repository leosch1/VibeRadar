resource "aws_ecr_repository" "api" {
  name = "vibe-radar-api"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "api_image_repository_url" {
  value = aws_ecr_repository.api.repository_url
}
