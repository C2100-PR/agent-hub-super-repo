#!/bin/bash
set -e

echo "Verifying Pinecone configuration..."

# Check Pinecone index
echo "Checking Pinecone index in us-central1..."
curl -X GET \
  "https://api.pinecone.io/indexes/dr-lucy-knowledge" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json"

# Verify each namespace
for NS in "primary" "secondary" "tertiary"; do
  echo "Checking namespace: $NS"
  curl -X POST \
    "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/describe_index_stats" \
    -H "Api-Key: ${PINECONE_API_KEY}" \
    -H "Accept: application/json" \
    -d "{\"namespace\": \"$NS\"}"
done

# Test vector operations
echo "Testing vector operations..."
curl -X POST \
  "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/query" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json" \
  -d "{
    \"namespace\": \"primary\",
    \"top_k\": 1,
    \"vector\": [0.1, 0.2, 0.3]
  }"

echo "Pinecone verification complete!"