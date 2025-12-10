locals {
  services = {
    genai_api = {
      service_name = "genai-api"
      service_port = 8080
      env_vars = {
        "GOOGLE_CLOUD_PROJECT"  = var.project_id
        "GOOGLE_CLOUD_LOCATION" = var.region
      }
    }
  }
}

resource "google_cloud_run_v2_service" "default" {
  for_each = local.services

  project  = var.project_id
  location = var.region
  name     = each.value.service_name

  template {
    service_account = google_service_account.cloud_run.email

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-learning-path-genai/${each.value.service_name}:latest"

      ports {
        container_port = each.value.service_port
      }

      dynamic "env" {
        for_each = each.value.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }
    }
  }

  # Ensure the image exists before creating the service
  depends_on = [google_artifact_registry_repository.learning_path_genai]
}
