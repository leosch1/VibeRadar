terraform {
  backend "s3" {
    bucket         = "vibe-radar-aws-terraform-state"
    key            = "aws.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    use_lockfile   = true
  }
}

provider "aws" {
  region = "eu-central-1"
}

module "vibe-radar" {
  source = "../../resources"
}
