#!/bin/bash

# Dr. Lucy Launch Script
# This script handles the launch sequence for Dr. Lucy endpoints

set -e

echo "Starting Dr. Lucy launch sequence..."

# Verify service accounts
for SA in $(yq e '.service_accounts[]' config/dr-lucy/launch.yaml); do
  echo "Verifying service account: $SA"
  gcloud iam service-accounts get-iam-policy $SA
done

# Check endpoints
for ENDPOINT in $(yq e '.endpoints[]' config/dr-lucy/launch.yaml); do
  ID=$(echo $ENDPOINT | yq e '.id')
  NAME=$(echo $ENDPOINT | yq e '.name')
  echo "Validating endpoint $NAME ($ID)"
  gcloud ai endpoints describe $ID --region=us-west1
done

# Verify network configuration
echo "Checking load balancer configuration..."
gcloud compute forwarding-rules list

# Launch sequence
echo "Initiating launch sequence..."
for ENDPOINT in $(yq e '.endpoints[]' config/dr-lucy/launch.yaml); do
  ID=$(echo $ENDPOINT | yq e '.id')
  gcloud ai endpoints deploy-model $ID \
    --region=us-west1 \
    --display-name="Dr-Lucy-Launch" \
    --service-account="drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com"
done

echo "Dr. Lucy launch complete!"