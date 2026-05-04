# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (BROWSER)                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                      Website (Frontend)                        │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │ HTML/CSS/JavaScript                                      │ │  │
│  │  │ - Upload Image Form                                      │ │  │
│  │  │ - Image Display                                          │ │  │
│  │  │ - Translate Text Display                                 │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                        │
│                              │ HTTP/HTTPS Requests                    │
│                              ▼                                        │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ API Calls
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AWS API GATEWAY                                   │
│              (Serverless REST API Endpoint)                          │
│  https://v9c90wf7fj.execute-api.us-east-1.amazonaws.com/api/       │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AWS LAMBDA (Chalice App)                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              Capabilities-dev Function                        │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │ Routes:                                                  │ │  │
│  │  │ POST /images          → upload_image()                  │ │  │
│  │  │ POST /images/{id}/translate-text → translate_image_text │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                    │                    │
                    │                    │
        ┌───────────┼─────────────────┬──┴──────────┐
        │           │                 │             │
        ▼           ▼                 ▼             ▼
    ┌────────┐ ┌──────────┐ ┌──────────────┐ ┌────────────┐
    │   S3   │ │ Translate│ │  Rekognition │ │   Polly    │
    │ Bucket │ │ Service  │ │   Service    │ │  Service   │
    │        │ │          │ │              │ │            │
    │ Stores │ │Translates│ │ Detects Text │ │ Text-to-   │
    │ Images │ │  Text    │ │  in Images   │ │ Speech     │
    └────────┘ └──────────┘ └──────────────┘ └────────────┘
```

## Service Components

### 1. Frontend Layer
- **Technology**: HTML5, CSS3, JavaScript
- **Location**: `website/` folder
- **Responsibilities**:
  - Serve static website
  - User interface for image upload
  - Display results
  - Handle form validation
  - Communicate with API

### 2. API Layer
- **Technology**: Chalice Framework (Python)
- **Location**: `Capabilities/app.py`
- **Endpoints**:
  - `POST /images` - Upload image to S3
  - `POST /images/{image_id}/translate-text` - Detect and translate text
- **Features**:
  - CORS enabled
  - Error handling
  - Request/response formatting

### 3. Business Logic (Services)

```
┌─────────────────────────────────────────────────────┐
│              Chalicelib Services                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ storage_service.py                           │  │
│  │ - Uploads files to S3                        │  │
│  │ - Generates signed URLs                      │  │
│  │ - Returns file metadata                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ recognition_service.py                       │  │
│  │ - Detects text in images (Rekognition)      │  │
│  │ - Filters by confidence threshold            │  │
│  │ - Returns text with bounding boxes           │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ translation_service.py                       │  │
│  │ - Translates text using AWS Translate       │  │
│  │ - Supports multiple language pairs           │  │
│  │ - Returns translated text                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ polly_service.py                             │  │
│  │ - Converts text to speech (AWS Polly)        │  │
│  │ - Returns MP3 audio bytes                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ aws_config.py                                │  │
│  │ - AWS region configuration                   │  │
│  │ - Reads from environment variables           │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4. AWS Services

| Service | Purpose | Usage |
|---------|---------|-------|
| **S3** | Image Storage | Store uploaded images, serve via signed URLs |
| **Translate** | Text Translation | Translate detected text to English |
| **Rekognition** | Image Analysis | Detect text in images |
| **Polly** | Text-to-Speech | Convert text to audio (optional) |
| **Lambda** | Serverless Compute | Run Chalice app |
| **API Gateway** | REST API | Expose Lambda functions via HTTP |
| **IAM** | Access Control | Manage permissions for Lambda functions |
| **CloudWatch** | Logging | Monitor Lambda execution and errors |

## Data Flow

```
User Workflow:
1. User uploads image via website
   ▼
2. Browser sends POST /images with base64-encoded image
   ▼
3. Lambda function receives request
   ▼
4. StorageService uploads image to S3
   ▼
5. API returns signed URL for image display
   ▼
6. Browser displays image
   ▼
7. User clicks "Translate" button
   ▼
8. Browser sends POST /images/{id}/translate-text
   ▼
9. Lambda executes:
   - RecognitionService.detect_text() → Rekognition API
   - TranslationService.translate_text() → Translate API
   ▼
10. Results returned to browser
    ▼
11. Website displays translated text
```

## Deployment Architecture

```
┌──────────────────────────────┐
│    Local Development         │
├──────────────────────────────┤
│ make test                    │
│ make docker-build            │
│ make docker-run              │
└──────────────────────────────┘
         │
         │ git push
         ▼
┌──────────────────────────────┐
│  GitHub Actions CI/CD        │
├──────────────────────────────┤
│ ✓ Run tests                  │
│ ✓ Build Docker image         │
│ ✓ Code quality checks        │
│ ✓ Security scans             │
└──────────────────────────────┘
         │
         │ chalice deploy
         ▼
┌──────────────────────────────┐
│   AWS Production             │
├──────────────────────────────┤
│ Lambda + API Gateway         │
│ S3 + Translate + Rekognition │
└──────────────────────────────┘
```

## Technology Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- Fetch API for HTTP requests

### Backend
- Python 3.11
- Chalice (AWS Serverless Framework)
- Boto3 (AWS SDK)

### Infrastructure
- AWS Lambda
- AWS API Gateway
- AWS S3
- AWS Translate
- AWS Rekognition
- AWS Polly
- AWS IAM
- AWS CloudWatch

### CI/CD & Containerization
- Docker (Multi-stage builds)
- GitHub Actions
- Git (Version Control)

### Testing
- Python unittest
- Pytest
- AWS service integration tests

## Security Considerations

```
┌─────────────────────────────────────────────────┐
│            Security Layers                      │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Frontend                                     │
│    - HTTPS only                                 │
│    - CORS enabled (controlled access)           │
│                                                 │
│ 2. API Gateway                                  │
│    - Authentication via IAM                     │
│    - Rate limiting (optional)                   │
│    - Request validation                         │
│                                                 │
│ 3. Lambda Function                              │
│    - IAM role with minimal permissions          │
│    - Environment variables for secrets          │
│    - Input validation                           │
│                                                 │
│ 4. AWS Services                                 │
│    - S3 bucket with signed URLs                 │
│    - Proper IAM permissions                     │
│    - Encrypted data in transit (HTTPS)          │
│                                                 │
│ 5. Secrets Management                           │
│    - GitHub Secrets for credentials             │
│    - Environment variables in Lambda            │
│    - No hardcoded secrets                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Scaling & Performance

- **Lambda**: Auto-scales based on concurrent requests
- **API Gateway**: Handles routing and DDoS protection
- **S3**: Highly available storage (99.99% uptime)
- **Signed URLs**: Prevent bandwidth waste with temporary access
- **Regional Deployment**: us-east-1 region for all services

## Cost Optimization

- **Lambda**: Pay per execution (free tier: 1M requests/month)
- **S3**: Pay per GB stored + data transfer
- **Translate**: Pay per character translated
- **Rekognition**: Pay per image processed
- **Polly**: Pay per character synthesized (if used)

## Future Enhancements

1. **Caching**: CloudFront for static assets
2. **Database**: DynamoDB for metadata storage
3. **Queue**: SQS for async processing
4. **Monitoring**: X-Ray for tracing requests
5. **CDN**: CloudFront for global distribution
6. **Multi-region**: Replicate to multiple AWS regions
