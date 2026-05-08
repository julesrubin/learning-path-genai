locals {
  services = {
    genai_api = {
      service_name = "genai-api-${local.branch_name_sanitized}"
      image_name   = "genai-api" # Base image name without branch
      service_port = 8080
      env_vars = {
        "GOOGLE_CLOUD_PROJECT"    = var.project_id
        "GOOGLE_CLOUD_LOCATION"   = var.region
        "RAG_CORPUS_DISPLAY_NAME" = local.rag_corpus_display_name
      }
    }
  }
}

resource "google_cloud_run_v2_service" "default" {
  for_each = local.services

  project             = var.project_id
  location            = var.region
  name                = each.value.service_name
  deletion_protection = false

  template {
    service_account = google_service_account.cloud_run.email

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-learning-path-genai-${local.branch_name_sanitized}/${each.value.image_name}:latest"

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

  depends_on = [
    google_artifact_registry_repository.learning_path_genai,
    google_project_iam_member.cloud_build_run_admin,
  ]
}
