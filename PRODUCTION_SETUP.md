# Production Setup Guide

This guide walks you through setting up AWS credentials and deploying to production.

## GitHub Secrets Configuration

The CI/CD pipeline requires AWS credentials to run tests. Follow these steps to add them:

### Step 1: Create AWS IAM User (Recommended)

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Create user**
3. Name: `github-ci-cd` (or your preferred name)
4. Click **Next** → **Attach policies**
5. Attach these policies:
   - `AmazonPollyFullAccess` - For text-to-speech
   - `TranslateFullAccess` - For translation
   - `AmazonRekognitionFullAccess` - For image recognition
   - `AmazonS3FullAccess` - For S3 bucket operations
6. Click **Create user** → **Create access key**
7. Select **Local code** → **Create access key**
8. Copy the **Access Key ID** and **Secret Access Key**

### Step 2: Add Secrets to GitHub

1. Go to your GitHub repository: https://github.com/Anmol-Shrestha/aws-image-text-speech
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:

| Secret Name | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key |
| `AWS_REGION` | `us-east-1` (or your preferred region) |

### Step 3: Verify Secrets Are Set

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see all three secrets listed

## Environment Variables

The application uses these environment variables:

```bash
AWS_ACCESS_KEY_ID          # AWS IAM user access key
AWS_SECRET_ACCESS_KEY      # AWS IAM user secret key
AWS_REGION                 # AWS region (defaults to us-east-1)
```

## Testing Locally with AWS Credentials

To test locally with your AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1

make test
```

Or use AWS CLI credentials:

```bash
aws configure  # This sets up ~/.aws/credentials
make test      # Will use configured AWS credentials
```

## Deployment Checklist

Before deploying to production:

- [ ] AWS IAM user created with appropriate permissions
- [ ] GitHub Secrets configured (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
- [ ] S3 bucket created and accessible
- [ ] Tests passing in CI/CD pipeline
- [ ] All GitHub Actions workflows showing ✅
- [ ] Docker image builds successfully
- [ ] Code quality checks passing (pylint, black, isort)
- [ ] Security scans passing (bandit, safety)

## CI/CD Pipeline Status

Check the status of your workflows:
1. Go to **Actions** tab in your GitHub repository
2. View the latest workflow runs
3. Each job should show ✅ for success

## Troubleshooting

### Tests failing with "NoRegionError"
- Ensure `AWS_REGION` secret is set in GitHub
- Default region is `us-east-1`

### Tests failing with "Unable to locate credentials"
- Verify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` secrets are set
- Check IAM user has appropriate permissions

### AWS API permission denied errors
- Verify IAM user has these permissions:
  - `polly:SynthesizeSpeech`
  - `translate:TranslateText`
  - `rekognition:DetectText`
  - `s3:PutObject`, `s3:GetObject`

## AWS Best Practices

1. **Use IAM Roles (Advanced)**: For production, use AWS OIDC with GitHub instead of long-lived credentials
2. **Rotate Credentials**: Regularly rotate access keys
3. **Least Privilege**: Only grant necessary permissions to the IAM user
4. **Monitor**: Use AWS CloudTrail to monitor API calls from CI/CD
5. **Secrets Management**: Never commit credentials to git

## Deploying with Chalice

To deploy the Chalice app to AWS Lambda:

```bash
cd Capabilities
chalice deploy
```

This will:
1. Package the application
2. Create/update Lambda functions
3. Set up API Gateway endpoints
4. Deploy to AWS

## Additional Resources

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS Chalice Documentation](https://aws.github.io/chalice/)
