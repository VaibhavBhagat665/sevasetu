#!/bin/bash
# SevaSetu — AWS Resource Setup Script
# Run this ONCE on your EC2 instance to create all required AWS resources.
# Prerequisites: AWS CLI configured with appropriate permissions.

set -e

REGION="ap-south-1"
DOCUMENTS_BUCKET="sevasetu-documents"
FORMS_BUCKET="sevasetu-forms"
DYNAMO_TABLE="sevasetu-sessions"

echo "============================================"
echo " SevaSetu — AWS Resource Setup"
echo "============================================"

# 1. Create S3 Buckets
echo ""
echo "[1/3] Creating S3 buckets..."

aws s3 mb s3://$DOCUMENTS_BUCKET --region $REGION 2>/dev/null && \
    echo "  ✓ Created bucket: $DOCUMENTS_BUCKET" || \
    echo "  ⚠ Bucket $DOCUMENTS_BUCKET already exists (or name taken)"

aws s3 mb s3://$FORMS_BUCKET --region $REGION 2>/dev/null && \
    echo "  ✓ Created bucket: $FORMS_BUCKET" || \
    echo "  ⚠ Bucket $FORMS_BUCKET already exists (or name taken)"

# Set CORS on forms bucket (for PDF download from browser)
echo '{"CORSRules":[{"AllowedHeaders":["*"],"AllowedMethods":["GET"],"AllowedOrigins":["*"],"MaxAgeSeconds":3600}]}' > /tmp/cors.json
aws s3api put-bucket-cors --bucket $FORMS_BUCKET --cors-configuration file:///tmp/cors.json
echo "  ✓ CORS configured on $FORMS_BUCKET"

# 2. Create DynamoDB Table
echo ""
echo "[2/3] Creating DynamoDB table..."

aws dynamodb create-table \
    --table-name $DYNAMO_TABLE \
    --attribute-definitions AttributeName=session_id,AttributeType=S \
    --key-schema AttributeName=session_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && \
    echo "  ✓ Created table: $DYNAMO_TABLE" || \
    echo "  ⚠ Table $DYNAMO_TABLE already exists"

# 3. Verify Bedrock model access
echo ""
echo "[3/3] Checking Bedrock model access..."
aws bedrock list-foundation-models --region $REGION --query "modelSummaries[?modelId=='anthropic.claude-3-haiku-20240307-v1:0'].modelId" --output text 2>/dev/null && \
    echo "  ✓ Claude 3 Haiku is available" || \
    echo "  ⚠ Please enable Bedrock model access in the AWS Console"

echo ""
echo "============================================"
echo " Setup complete!"
echo " S3 buckets: $DOCUMENTS_BUCKET, $FORMS_BUCKET"
echo " DynamoDB:   $DYNAMO_TABLE"
echo " Region:     $REGION"
echo "============================================"
echo ""
echo "Next: Run 'docker-compose up -d --build' to start the app."
