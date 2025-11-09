#!/bin/bash

# Deploy to hackathon-wildfire-epsilon.limited S3 bucket
set -e

BUCKET_NAME="hackathon-wildfire-epsilon.limited"
REGION="us-east-1"
AWS_PROFILE="epsilon"

echo "🔥 Deploying to S3 bucket: ${BUCKET_NAME}"
echo "Using AWS profile: ${AWS_PROFILE}"
echo "Region: ${REGION}"
echo "================================================"

# Check if bucket exists
echo "Checking if bucket exists..."
if ! aws s3 ls "s3://${BUCKET_NAME}" --profile ${AWS_PROFILE} 2>/dev/null; then
    echo "Error: Bucket ${BUCKET_NAME} does not exist or you don't have access"
    exit 1
fi

# # Disable Block Public Access settings FIRST
# echo "Disabling Block Public Access settings..."
# aws s3api put-public-access-block \
#     --bucket ${BUCKET_NAME} \
#     --public-access-block-configuration \
#     "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false" \
#     --profile ${AWS_PROFILE}

# # Enable static website hosting
# echo "Enabling static website hosting..."
# aws s3 website "s3://${BUCKET_NAME}" \
#     --index-document index.html \
#     --error-document index.html \
#     --profile ${AWS_PROFILE}

# # Set bucket policy for public access
# echo "Setting bucket policy for public access..."
# cat > /tmp/bucket-policy.json <<EOF
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "PublicReadGetObject",
#             "Effect": "Allow",
#             "Principal": "*",
#             "Action": "s3:GetObject",
#             "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
#         }
#     ]
# }
# EOF

# aws s3api put-bucket-policy \
#     --bucket ${BUCKET_NAME} \
#     --policy file:///tmp/bucket-policy.json \
#     --profile ${AWS_PROFILE}

# Upload files
echo "Uploading files to S3..."
aws s3 sync . "s3://${BUCKET_NAME}/" \
    --exclude ".DS_Store" \
    --exclude "*.md" \
    --exclude "*.sh" \
    --exclude ".git/*" \
    --cache-control "public, max-age=3600" \
    --delete \
    --profile ${AWS_PROFILE}

# Set correct content types for specific files
echo "Setting content types..."
aws s3 cp "s3://${BUCKET_NAME}/css/" "s3://${BUCKET_NAME}/css/" \
    --exclude "*" --include "*.css" \
    --content-type "text/css" \
    --metadata-directive REPLACE \
    --recursive \
    --profile ${AWS_PROFILE} 2>/dev/null || true

aws s3 cp "s3://${BUCKET_NAME}/js/" "s3://${BUCKET_NAME}/js/" \
    --exclude "*" --include "*.js" \
    --content-type "application/javascript" \
    --metadata-directive REPLACE \
    --recursive \
    --profile ${AWS_PROFILE} 2>/dev/null || true

# # Get the website URL
# WEBSITE_URL="http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com"

echo ""
echo "================================================"
echo "✅ Deployment complete!"
echo ""
echo "Website URL: ${WEBSITE_URL}"
echo ""
echo "Note: If the URL doesn't work, check your bucket's region."
echo "Your bucket might be in a different region than ${REGION}."
echo ""
