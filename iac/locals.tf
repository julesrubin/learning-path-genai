locals {
  # Sanitize branch name for GCP resource naming (replace _ with -)
  # GCP resource IDs only allow lowercase letters, numbers, and hyphens
  branch_name_sanitized = substr(replace(var.branch_name, "_", "-"), 0, 20) # Limit branch suffix length

  # Single source of truth for the RAG corpus display name. Consumed by both
  # the Cloud Run service (env var) and the bootstrap script (via terraform output).
  rag_corpus_display_name = "styleco-knowledge-base-${local.branch_name_sanitized}"
}
