provider "aws" {
  region  = "${var.aws_region}"
  profile = "${var.profile}"
  version = "= 1.9.0"
}

provider "template" {
  version = "= 1.0"
}

terraform {
  terragrunt_version = "0.14.0"
  required_version   = "= 0.11.3"

  backend "s3" {}
}
