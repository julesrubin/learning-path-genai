# Vertex AI RAG Engine — IAM only.

data "google_project" "current" {
  project_id = var.project_id
}

# The Vertex AI Service Agent reads from the bucket during corpus ingestion.
resource "google_storage_bucket_iam_member" "rag_agent_reader" {
  bucket = google_storage_bucket.rag_documents.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:service-${data.google_project.current.number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
}
