#!/bin/bash
set -e

echo "=== Verifying Pinecone Memory Workload Setup ==="

# Check index status and configuration
echo "1. Checking index configuration..."
curl -X GET \
  "https://api.pinecone.io/indexes/dr-lucy-knowledge" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json"

# Verify each namespace memory allocation
for NS in "primary" "secondary" "tertiary"; do
  echo "2. Checking namespace: $NS"
  curl -X POST \
    "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/describe_index_stats" \
    -H "Api-Key: ${PINECONE_API_KEY}" \
    -H "Accept: application/json" \
    -d "{\"namespace\": \"$NS\"}"
done

# Test vector operations with memory tracking
echo "3. Testing vector operations with memory usage..."
curl -X POST \
  "https://dr-lucy-knowledge-${INDEX_ID}.svc.us-central1-gcp.pinecone.io/query" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json" \
  -d "{
    \"namespace\": \"primary\",
    \"top_k\": 1,
    \"vector\": [0.1, 0.2, 0.3],
    \"include_metadata\": true
  }"

# Get memory utilization metrics
echo "4. Checking memory utilization..."
curl -X GET \
  "https://api.pinecone.io/metrics/dr-lucy-knowledge" \
  -H "Api-Key: ${PINECONE_API_KEY}" \
  -H "Accept: application/json"

echo "Memory workload verification complete."