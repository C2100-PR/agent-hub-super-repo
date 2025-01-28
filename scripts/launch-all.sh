#!/bin/bash
set -e

echo "Starting launch sequence..."

# Using the primary service account
SERVICE_ACCOUNT="drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com"

# Launch Dr. Lucy agents in us-west1
echo "Launching Dr. Lucy agents..."

# Dr-Lucy-01
echo "Launching Dr-Lucy-01..."
gcloud ai endpoints deploy-model 6296186210691842048 \
  --region=us-west1 \
  --service-account=$SERVICE_ACCOUNT

# Dr-Lucy-02
echo "Launching Dr-Lucy-02..."
gcloud ai endpoints deploy-model 6301815710226055168 \
  --region=us-west1 \
  --service-account=$SERVICE_ACCOUNT

# Dr-Lucy-03
echo "Launching Dr-Lucy-03..."
gcloud ai endpoints deploy-model 3426267348149993472 \
  --region=us-west1 \
  --service-account=$SERVICE_ACCOUNT

# Launch Super Claude 1 in us-west4
echo "Launching Super Claude 1..."
gcloud ai endpoints deploy-model 4313929473532624896 \
  --region=us-west4 \
  --service-account=$SERVICE_ACCOUNT

# Verify all endpoints
echo "Verifying endpoints..."
for REGION in us-west1 us-west4; do
  echo "Checking $REGION..."
  gcloud ai endpoints list --region=$REGION
done

echo "Launch sequence complete!"