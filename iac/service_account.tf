resource "google_service_account" "cloud_run" {
  project      = var.project_id
  account_id   = "cloud-run-sa-${local.branch_name_sanitized}"
  display_name = "Cloud Run Service Account"
  description  = "Service account for Cloud Run services with Vertex AI access"
}
