# Cloud Run service account needs Vertex AI access to call Gemini
resource "google_project_iam_member" "cloud_run_vertex_ai" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Cloud Build service account needs to "act as" Cloud Run service account
# This is required to deploy Cloud Run services that use cloud-run-sa
resource "google_service_account_iam_member" "cloud_build_act_as_cloud_run" {
  service_account_id = google_service_account.cloud_run.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Cloud Build service account needs Cloud Run admin to create/update services
# Granted via terraform so it's available when students enable Cloud Run deployment
resource "google_project_iam_member" "cloud_build_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}
