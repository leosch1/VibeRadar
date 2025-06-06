data "aws_caller_identity" "current" {}

resource "aws_iam_user" "github" {
  name = "vibe-radar-github-actions"
}

resource "aws_iam_access_key" "github" {
  user = aws_iam_user.github.name
}

resource "aws_iam_policy" "github_actions_deploy" {
  name = "GitHubActionsDeployPolicy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [

      # --- ECS: full write required for task lifecycle ---
      {
        Effect = "Allow",
        Action = [
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService",
          "ecs:DeregisterTaskDefinition"
        ],
        Resource = "*"
      },

      # --- IAM PassRole (used by ECS tasks to assume execution role) ---
      {
        Effect = "Allow",
        Action = [
          "iam:PassRole"
        ],
        Resource = format(
          "arn:aws:iam::%s:role/vibe-radar-ecs-execution-role",
          data.aws_caller_identity.current.account_id
        )
      },

      # --- ECR: push and login ---
      {
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart"
        ],
        Resource = format(
          "arn:aws:ecr:eu-central-1:%s:repository/vibe-radar-api",
          data.aws_caller_identity.current.account_id
        )
      },

      # --- S3: access for Terraform state backend ---
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::vibe-radar-terraform-state-bucket-20250509224107982000000001",
          "arn:aws:s3:::vibe-radar-terraform-state-bucket-20250509224107982000000001/*",
          "arn:aws:s3:::vibe-radar-frontend-20250509230404820000000001",
          "arn:aws:s3:::vibe-radar-frontend-20250509230404820000000001/*"
        ]
      },

      # --- CloudFront ---
      {
        Effect = "Allow",
        Action = [
          "cloudfront:CreateInvalidation"
        ],
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_user_policy_attachment" "github_readonly" {
  user       = aws_iam_user.github.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}

resource "aws_iam_user_policy_attachment" "github_write" {
  user       = aws_iam_user.github.name
  policy_arn = aws_iam_policy.github_actions_deploy.arn
}
