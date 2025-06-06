variable "db_username" {
  description = "RDS Postgres username"
  default     = "postgres"
}

variable "db_password" {
  description = "RDS Postgres password"
  default     = "postgres"
  sensitive   = true
}

variable "api_image_url" {
  description = "Full ECR image with tag"
}

variable "domain_name" {
  description = "The root domain name"
  type        = string
  default     = "viberadar.io"
}

variable "backend_subdomain" {
  description = "Subdomain for the backend API"
  type        = string
  default     = "api"
}

variable "posthog_api_key" {
  description = "API key for posthog"
  type        = string
  sensitive   = true
}
