locals {
  # Sanitize branch name for GCP resource naming (replace _ with -)
  # GCP resource IDs only allow lowercase letters, numbers, and hyphens
  branch_name_sanitized = substr(replace(var.branch_name, "_", "-"),0, 20)  # Limit branch suffix length
}
