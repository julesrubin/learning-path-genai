#!/bin/bash
# Initialize resources before using Terraform
# Usage: ./init.sh [PROJECT_ID]
# If PROJECT_ID is not provided, uses current gcloud config

set -e

if [ -z "$1" ]; then
  PROJECT_ID=$(gcloud config get-value project)
else
  PROJECT_ID=$1
fi

TERRAFORM_BUCKET="${PROJECT_ID}-learning-path-tfstate"

echo "******"
echo "Project ID: $PROJECT_ID"
echo "Terraform state bucket: $TERRAFORM_BUCKET"
echo "******"

# Create Terraform state bucket if it doesn't exist
if ! gsutil ls -b "gs://$TERRAFORM_BUCKET" &>/dev/null; then
  echo "Creating Terraform state bucket..."
  gsutil mb -l eu -p "$PROJECT_ID" "gs://$TERRAFORM_BUCKET"
  gsutil versioning set on "gs://$TERRAFORM_BUCKET"
else
  echo "Terraform state bucket already exists"
fi

# Generate backend config
echo "bucket = \"$TERRAFORM_BUCKET\"" > backend.tfvars

echo "******"
echo "Backend config written to backend.tfvars"
echo "Run: terraform init -backend-config=init/backend.tfvars"
echo "******"
