variable "project_id" {
  type        = string
  description = "GCP project identifier"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "europe-west1"
}

variable "location" {
  type        = string
  description = "GCP location for multi-regional resources"
  default     = "EU"
}

variable "branch_name" {
  type        = string
  description = "Git branch name from Cloud Build (passed as TF_VAR_branch_name)"
}
