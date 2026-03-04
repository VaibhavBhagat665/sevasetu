"""
SevaSetu — AWS Configuration
Centralized AWS client initialization for S3, DynamoDB, and Bedrock.
"""

import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")  # Mumbai region (closest to India)
S3_BUCKET_DOCUMENTS = os.getenv("S3_BUCKET_DOCUMENTS", "sevasetu-documents")
S3_BUCKET_FORMS = os.getenv("S3_BUCKET_FORMS", "sevasetu-forms")
DYNAMO_TABLE_SESSIONS = os.getenv("DYNAMO_TABLE_SESSIONS", "sevasetu-sessions")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

# Track if AWS is available
_aws_available = False

try:
    _session = boto3.Session(region_name=AWS_REGION)
    # Test credentials
    _session.client("sts").get_caller_identity()
    _aws_available = True
    print(f"[AWS] Connected to AWS in region {AWS_REGION}")
except Exception as e:
    print(f"[AWS] AWS credentials not configured ({e}). Running in local/offline mode.")
    _aws_available = False


def is_aws_available():
    """Check if AWS credentials are properly configured."""
    return _aws_available


def get_s3_client():
    """Get S3 client."""
    if not _aws_available:
        return None
    return _session.client("s3")


def get_dynamodb_resource():
    """Get DynamoDB resource."""
    if not _aws_available:
        return None
    return _session.resource("dynamodb")


def get_bedrock_client():
    """Get Bedrock Runtime client."""
    if not _aws_available:
        return None
    return _session.client("bedrock-runtime")


def get_presigned_url(bucket, key, expiration=3600):
    """Generate a pre-signed S3 URL for downloading."""
    s3 = get_s3_client()
    if not s3:
        return None
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        print(f"[AWS] Pre-signed URL error: {e}")
        return None
