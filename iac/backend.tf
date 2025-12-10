terraform {
  required_version = ">= 1.14.1"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.13.0"
    }
  }
  backend "gcs" {}
}

provider "google" {
  project = var.project_id
  region  = var.region
}
