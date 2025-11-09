# S3 Static Site Deployment Guide

This guide shows how to deploy the Wildfire Fuel Mapping viewer as a static website on AWS S3.

## Prerequisites

- AWS Account
- AWS CLI installed and configured (`aws configure`)
- Your static site files are ready in the `static_site/` directory

## Directory Structure

```
static_site/
├── index.html                  # Main page
├── css/
│   └── style.css              # Styles
├── js/
│   └── main.js                # JavaScript (no API calls, static data)
├── maps/                       # Individual map visualizations
│   ├── 01_overview.html
│   ├── 02_change_detection.html
│   ├── 03_prediction.html
│   ├── 04_validation.html
│   ├── 05_summary.html
│   └── results_viewer.html
└── presentation/               # PNG images
    ├── 01_overview.png
    ├── 02_change_detection.png
    ├── 03_prediction.png
    ├── 04_validation.png
    └── 05_summary.png
```

## Deployment Steps

### Option 1: AWS Console (Manual)

1. **Create S3 Bucket**
   - Go to AWS S3 Console
   - Click "Create bucket"
   - Bucket name: `wildfire-fuel-mapping` (must be globally unique)
   - Region: Choose your preferred region (e.g., `us-west-2`)
   - **Uncheck** "Block all public access" (we need this for website hosting)
   - Acknowledge the warning
   - Click "Create bucket"

2. **Enable Static Website Hosting**
   - Select your bucket
   - Go to "Properties" tab
   - Scroll to "Static website hosting"
   - Click "Edit"
   - Select "Enable"
   - Index document: `index.html`
   - Error document: `index.html` (optional)
   - Click "Save changes"
   - **Note the endpoint URL** (e.g., `http://wildfire-fuel-mapping.s3-website-us-west-2.amazonaws.com`)

3. **Set Bucket Policy for Public Access**
   - Go to "Permissions" tab
   - Scroll to "Bucket policy"
   - Click "Edit"
   - Paste this policy (replace `YOUR-BUCKET-NAME`):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

4. **Upload Files**
   - Go to "Objects" tab
   - Click "Upload"
   - Drag and drop all files from `static_site/` maintaining directory structure
   - Click "Upload"

5. **Access Your Site**
   - Go to "Properties" > "Static website hosting"
   - Click on the "Bucket website endpoint" URL
   - Your site should now be live!

### Option 2: AWS CLI (Automated)

```bash
# Navigate to the webapp directory
cd /Users/thomasduquemin/epsilon/applications/hackathon/webapp

# Set your bucket name (must be globally unique)
BUCKET_NAME="wildfire-fuel-mapping-$(date +%s)"

# Create the bucket
aws s3 mb s3://${BUCKET_NAME} --region us-west-2

# Enable static website hosting
aws s3 website s3://${BUCKET_NAME} \
    --index-document index.html \
    --error-document index.html

# Set bucket policy for public access
cat > /tmp/bucket-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy \
    --bucket ${BUCKET_NAME} \
    --policy file:///tmp/bucket-policy.json

# Upload all files
aws s3 sync static_site/ s3://${BUCKET_NAME}/ \
    --exclude ".DS_Store" \
    --exclude "*.md" \
    --cache-control "public, max-age=3600"

# Get the website URL
echo "Website URL: http://${BUCKET_NAME}.s3-website-us-west-2.amazonaws.com"
```

### Option 3: CloudFront + S3 (Recommended for Production)

For better performance, HTTPS, and custom domain:

```bash
# After creating S3 bucket and uploading files...

# Create CloudFront distribution
aws cloudfront create-distribution \
    --origin-domain-name ${BUCKET_NAME}.s3-website-us-west-2.amazonaws.com \
    --default-root-object index.html

# This will return a CloudFront domain name like: d1234567890abc.cloudfront.net
```

**Benefits:**
- HTTPS by default
- Global CDN (faster worldwide)
- Custom domain support (e.g., `maps.yourcompany.com`)
- Better caching and compression

## Cost Estimate

**S3 Only:**
- Storage: ~10 MB = $0.00023/month
- Data transfer (first 100GB free): $0.00
- **Total: < $0.01/month** for low traffic

**With CloudFront:**
- First 1 TB data transfer: $0.085/GB
- First 10M requests: $0.01 per 10K
- **Total: ~$1-5/month** depending on traffic

## Custom Domain Setup (Optional)

1. **Register/Use Your Domain** (e.g., Route 53, Namecheap)

2. **Point Domain to CloudFront**
   - Create CNAME record: `maps.yourcompany.com` → CloudFront domain
   - Or for root domain: Use Route 53 Alias record

3. **Add SSL Certificate** (via AWS Certificate Manager - free!)
   ```bash
   aws acm request-certificate \
       --domain-name maps.yourcompany.com \
       --validation-method DNS
   ```

## Updating Your Site

To update the site after making changes:

```bash
# Sync changes (only uploads modified files)
aws s3 sync static_site/ s3://${BUCKET_NAME}/ \
    --delete \
    --cache-control "public, max-age=3600"

# If using CloudFront, invalidate cache
aws cloudfront create-invalidation \
    --distribution-id YOUR_DISTRIBUTION_ID \
    --paths "/*"
```

## Security Best Practices

1. **Enable S3 versioning** (protects against accidental deletion)
   ```bash
   aws s3api put-bucket-versioning \
       --bucket ${BUCKET_NAME} \
       --versioning-configuration Status=Enabled
   ```

2. **Enable S3 logging** (track access)
   ```bash
   aws s3api put-bucket-logging \
       --bucket ${BUCKET_NAME} \
       --bucket-logging-status file://logging.json
   ```

3. **Add CloudFront for HTTPS** (encrypts traffic)

4. **Use CloudFront signed URLs** (if you need access control)

## Troubleshooting

**Issue: 403 Forbidden Error**
- Check bucket policy allows public read
- Verify all files uploaded correctly
- Check S3 Block Public Access settings

**Issue: 404 Not Found for subpages**
- Ensure Error document is set to `index.html`
- Verify all HTML files uploaded to correct paths

**Issue: Images not loading**
- Check relative paths in HTML files
- Verify images uploaded to `presentation/` directory
- Check browser console for 404 errors

**Issue: CSS not loading**
- Verify CSS file uploaded to `css/style.css`
- Check Content-Type metadata: `text/css`
- Try clearing browser cache

## Monitoring

**View access logs:**
```bash
aws s3 ls s3://${BUCKET_NAME}-logs/
```

**Check bandwidth usage:**
- Go to S3 Console > Metrics tab
- View "Data transfer" and "Storage" metrics

## Deleting the Site

To completely remove everything:

```bash
# Delete all objects
aws s3 rm s3://${BUCKET_NAME} --recursive

# Delete bucket
aws s3 rb s3://${BUCKET_NAME}

# If using CloudFront, delete distribution first
aws cloudfront delete-distribution \
    --id YOUR_DISTRIBUTION_ID \
    --if-match ETAG
```

## Next Steps

1. Set up custom domain
2. Add CloudFront for HTTPS and performance
3. Set up CI/CD pipeline (GitHub Actions → S3)
4. Add Google Analytics or similar tracking
5. Consider adding CloudFront Functions for dynamic behavior

## Resources

- [S3 Static Website Hosting Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [Route 53 Documentation](https://docs.aws.amazon.com/route53/)
- [AWS Certificate Manager](https://docs.aws.amazon.com/acm/)
