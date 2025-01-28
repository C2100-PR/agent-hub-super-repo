#!/bin/bash
set -e

echo "Starting cautious verification of Dr-Lucy-01..."

# Step 1: Check endpoint status
echo "Checking endpoint status..."
STATUS=$(gcloud ai endpoints describe 6296186210691842048 \
  --region=us-west1 \
  --format="get(state)")

if [ "$STATUS" != "ACTIVE" ]; then
  echo "ERROR: Endpoint not active"
  exit 1
fi

# Step 2: Verify service account permissions
echo "Verifying service account..."
gcloud iam service-accounts get-iam-policy \
  drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com \
  --format="table(bindings.role,bindings.members)"

# Step 3: Test Pinecone connection
echo "Testing Pinecone connection..."
curl -X POST \
  "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/describe_index_stats" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  --fail \
  --silent \
  --show-error

# Step 4: Network validation
echo "Validating network..."
gcloud compute networks vpc-peerings list \
  --filter="network:vpc-dr-lucy" \
  --format="table(name,network1,network2,state)"

echo "Initial verification complete. Please review outputs before proceeding."