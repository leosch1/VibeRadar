terraform {
  backend "s3" {
    bucket         = "vibe-radar-terraform-state-bucket-20250509224107982000000001"
    key            = "app/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    use_lockfile   = true
  }
}
