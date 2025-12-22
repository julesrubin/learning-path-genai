locals {
  # Sanitize branch name for GCP resource naming (replace _ with -)
  # GCP resource IDs only allow lowercase letters, numbers, and hyphens
  branch_name_sanitized = replace(var.branch_name, "_", "-")
}
