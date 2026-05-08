resource "google_storage_bucket" "rag_documents" {
  name                        = "${var.project_id}-gcs-learning-path-genai-${local.branch_name_sanitized}"
  location                    = var.location
  project                     = var.project_id
  uniform_bucket_level_access = true
  force_destroy               = true
}

# Upload every file under data/styleco/ into the bucket, preserving folders.
resource "google_storage_bucket_object" "styleco_documents" {
  for_each = fileset("${path.module}/../data/styleco", "**/*")

  name   = "styleco/${each.value}"
  bucket = google_storage_bucket.rag_documents.name
  source = "${path.module}/../data/styleco/${each.value}"
}

# Cloud Run SA reads the bucket (for direct file lookups in citations).
resource "google_storage_bucket_iam_member" "cloud_run_rag_reader" {
  bucket = google_storage_bucket.rag_documents.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.cloud_run.email}"
}

# The Vertex AI Service Agent reads from the bucket during corpus ingestion.
resource "google_storage_bucket_iam_member" "rag_agent_reader" {
  bucket = google_storage_bucket.rag_documents.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:service-${var.project_number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
}

output "rag_documents_bucket" {
  description = "GCS bucket holding StyleCo source documents for RAG ingestion."
  value       = google_storage_bucket.rag_documents.name
}

output "rag_corpus_display_name" {
  description = "Display name of the RAG Engine corpus (used by the bootstrap script)."
  value       = local.rag_corpus_display_name
}
