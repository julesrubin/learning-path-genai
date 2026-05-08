# Vertex AI RAG Engine — project-level configuration and IAM.
#
# Terraform owns the project tier and the IAM grant for the Vertex AI Service
# Agent on the source bucket (defined in storage.tf).
#
# The corpus and file imports are NOT Terraform-managed — they live in
# `cloud_run/genai-api/scripts/bootstrap_rag_corpus.py` because the provider
# has no resource for them yet.

data "google_project" "current" {
  project_id = var.project_id
}

# The Vertex AI Service Agent reads from the bucket during corpus ingestion.
resource "google_storage_bucket_iam_member" "rag_agent_reader" {
  bucket = google_storage_bucket.rag_documents.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:service-${data.google_project.current.number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
}

# Project-level RAG Engine tier — `basic` is the cheapest, fine for dev.
resource "google_vertex_ai_rag_engine_config" "this" {
  project = var.project_id
  region  = var.region
  rag_managed_db_config {
    basic {}
  }
}
