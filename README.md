# Learning Path GenAI

Practical learning path for Generative AI development on Google Cloud Platform.

## Purpose

This path provides a hands-on journey to become proficient in GenAI development on GCP. Over 20-25 working days, you'll build a complete **AI-powered Customer Experience Platform** for a fictional fashion retailer called **StyleCo**.

## Target Audience

- **Experience**: Software development background
- **AI/ML**: Good acculturation to AI concepts, no prior implementation experience required
- **Python**: Primary language, but this is not a Python course
- **GCP**: Basic familiarity helpful but not required

## Learning Philosophy

Each chapter follows a three-part structure:

1. **Context**: Realistic business scenario tied to StyleCo
2. **Learning Resources**: Curated links to documentation and courses
3. **Mission**: Hands-on tasks producing working code

**Progressive Autonomy**: Early chapters are guided, later chapters are autonomous.

## Topics Covered

| Topic | Description |
|-------|-------------|
| LLM Fundamentals | Tokens, embeddings, prompting, temperature |
| Vertex AI Model Garden | Text, image, audio, video generation |
| Gemini Models | Model selection and best practices |
| RAG (Managed) | Vertex AI Search |
| RAG (Unmanaged) | Cloud SQL + pgvector, RAG Engine |
| Function Calling | Connecting LLMs to external APIs |
| MCP Servers | Model Context Protocol with Python SDK |
| ADK | Agent Development Kit basics |
| Advanced ADK | Multi-agent, state, memory, artifacts, callbacks |
| Responsible AI | Model Armor integration |
| MLOps for GenAI | Evaluation, monitoring, CI/CD |

## Topics NOT Covered

- Traditional ML model training
- Deep mathematical foundations of transformers
- Non-GCP platforms
- Fine-tuning foundation models

## Duration

**Total: 20-25 working days**

See [GitHub Issues](https://github.com/julesrubin/learning-path-genai/issues) for chapter details and progress.

## Prerequisites

- [ ] GCP Sandbox project with billing enabled
- [ ] VS Code or preferred IDE
- [ ] Python 3.11+
- [ ] Git configured with GitHub account
- [ ] gcloud CLI installed and authenticated

## Getting Started

### 1. Clone this repository

### 2. Create your own branch: 
`git checkout -b <your-branch-name> && git push --set-upstream origin <your-branch-name>`

### 3. Get Your Sandbox

Request a GCP sandbox project from your manager.

### 4. Install Tools
- VS Code (or preferred IDE)
- Python 3.11+
- Git
- gcloud CLI: https://cloud.google.com/sdk/docs/install-sdk

### 5. Authenticate
```bash
gcloud auth login
gcloud auth application-default login
```

### 6. Clone and Branch
```bash
git clone <repository-url>
cd learning-path-genai
git checkout -b <your-sandbox-project-id>
git push --set-upstream origin <your-sandbox-project-id>
```

### 7. Enable APIs
```bash
export PROJECT_ID=$(gcloud config get-value project)
gcloud services enable \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  --project $PROJECT_ID
```

### 8 Create a Service Account for Cloud Build
```bash
gcloud iam service-accounts create build-learning-path-sa \
  --display-name="Cloud Build Service Account" \
  --project=$PROJECT_ID
```

We also need to grant the service account the first necessary roles:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:build-learning-path-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:build-learning-path-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:build-learning-path-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:build-learning-path-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"
```

### 9. Set Up Cloud Build Trigger
1. Go to Cloud Build in GCP Console
2. Click Repositories > Connect Repository
3. Create a trigger for your branch to run on pushes
4. Select the service account created earlier
5. Let everything else as default and save your trigger
