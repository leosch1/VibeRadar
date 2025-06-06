resource "aws_iam_role" "ecs_task_execution" {
  name = "vibe-radar-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy" "ecs_cloudwatch_logs" {
  name        = "ECSCloudWatchLogsPolicy"
  description = "Least privilege policy for ECS to write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ],
        Resource = [
          "arn:aws:logs:eu-central-1:${data.aws_caller_identity.current.account_id}:log-group:/ecs/vibe-radar-api:*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_logs_least_privilege" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = aws_iam_policy.ecs_cloudwatch_logs.arn
}

resource "aws_ecs_cluster" "main" {
  name = "vibe-radar-cluster"
}

resource "aws_cloudwatch_log_group" "ecs_api" {
  name              = "/ecs/vibe-radar-api"
  retention_in_days = 14
}

resource "aws_security_group" "ecs" {
  name        = "vibe-radar-ecs-sg"
  description = "Allow ALB to access ECS tasks on port 8008"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "Allow traffic from ALB"
    from_port       = 8008
    to_port         = 8008
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_task_definition" "api" {
  family                   = "vibe-radar-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([{
    name      = "api"
    image     = var.api_image_url
    essential = true
    portMappings = [{
      containerPort = 8008
    }]
    environment = [
      {
        name  = "DATABASE_URL"
        value = "postgresql://postgres:${var.db_password}@${aws_db_instance.postgres.address}:5432/postgres"
      },
      {
        name  = "ALLOWED_ORIGINS"
        value = "https://viberadar.io,https://bdp25.github.io"
      },
      {
        name  = "POSTHOG_PROJECT_ID"
        value = "67446"
      },
      {
        name  = "POSTHOG_API_KEY"
        value = var.posthog_api_key
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.ecs_api.name
        awslogs-region        = "eu-central-1"
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "api" {
  name            = "vibe-radar-api"
  cluster         = aws_ecs_cluster.main.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.ecs.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8008
  }

  depends_on = [aws_lb_listener.api_https]
}
