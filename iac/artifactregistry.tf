resource "google_artifact_registry_repository" "learning_path_genai" {
  repository_id = "${var.project_id}-gcr-learning-path-genai"
  format        = "DOCKER"
  location      = var.region
  description   = "Docker repository for Cloud Run service images for the Learning Path GenAI."
  project       = var.project_id
}

output "artifact_registry_learning_path_genai_repo_url" {
  description = "The URL of the Docker Artifact Registry repository for Cloud Run images."
  value       = google_artifact_registry_repository.learning_path_genai.name
}
