# locals {
#   services = {
#     genai_api = {
#       service_name = "genai-api"
#       service_port = 8080
#     }
#   }
# }

# resource "google_cloud_run_v2_service" "default" {
#   for_each = local.services

#   project  = var.project_id
#   location = var.region
#   name     = each.value.service_name
#   template {
#     containers {
#       image = "${google_artifact_registry_repository.learning_path_genai.name}/${each.value.service_name}:latest"
#       ports {
#         container_port = each.value.service_port
#       }
#     }
#   }
# }
