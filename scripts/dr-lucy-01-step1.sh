#!/bin/bash
set -e

echo "=== Dr-Lucy-01 Verification Step 1 ==="
echo "Running minimal connectivity test..."

# Check endpoint health
echo "1. Endpoint Health Check (6296186210691842048)"
gcloud ai endpoints describe 6296186210691842048 \
  --region=us-west1 \
  --format="table(state,displayName,createTime)" || {
    echo "CRITICAL: Endpoint check failed"
    exit 1
  }

# Verify service account minimal access
echo "2. Service Account Basic Check"
gcloud iam service-accounts get-iam-policy \
  drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com \
  --format="table(bindings.role)" || {
    echo "CRITICAL: Service account check failed"
    exit 1
  }

# Test basic Pinecone connection
echo "3. Basic Pinecone Connection Test"
curl --max-time 5 \
  "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/health" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  --fail \
  --silent \
  --show-error || {
    echo "CRITICAL: Pinecone connection failed"
    exit 1
  }

echo "Initial verification complete. Review output before proceeding."