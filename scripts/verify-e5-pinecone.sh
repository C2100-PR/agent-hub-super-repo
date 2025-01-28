#!/bin/bash
set -e

PINECONE_INDEX="multilingual-e5-large"
PINECONE_ENV="gcp-us-central1-4a9f"
PINECONE_ENDPOINT="multilingual-e5-large-jgzrexs.svc.gcp-us-central1-4a9f.pinecone.io"

echo "=== Verifying E5 Pinecone Setup ==="

# Check index health
echo "1. Checking index health..."
curl -X GET \
  "https://$PINECONE_ENDPOINT/health" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json"

# Check index stats for each namespace
for NS in "primary" "secondary" "tertiary"; do
  echo "2. Checking namespace: $NS"
  curl -X POST \
    "https://$PINECONE_ENDPOINT/describe_index_stats" \
    -H "Api-Key: ${PINECONE_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"filter\": {\"namespace\": \"$NS\"}}"
done

# Test basic query
echo "3. Testing query functionality..."
curl -X POST \
  "https://$PINECONE_ENDPOINT/query" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"namespace\": \"primary\",
    \"top_k\": 1,
    \"include_metadata\": true,
    \"vector\": [0.1, 0.2, 0.3]
  }"

echo "Verification complete."