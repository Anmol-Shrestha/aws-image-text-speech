# Cloud Services

A cloud services application that uploads images and performs text translation using AWS services.

## Features

- **File Upload**: Upload files to AWS S3 using boto3
- - **AWS Recognition**: Detects what ever is in the image using AWS Rekognition
- **Translation**: Translate text using AWS Translate service
- **Text-to-Speech**: Convert text to speech using AWS Polly


## Prerequisites

- Python 3.11+
- AWS Account with credentials configured
- Docker (for containerized deployment)

## Installation

```bash
make install
```

## Local Development Workflow

### Step 1: Set Up AWS Credentials

```bash
# Configure AWS credentials (one-time setup)
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

### Step 2: Run Tests Locally (Quick Feedback)

```bash
# Run tests (fast - 2-5 seconds)
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage report
make test-coverage
```

### Step 3: Build and Run Docker Locally

```bash
# Build Docker image (validates Docker build works locally)
make docker-build

# Run the Chalice API in Docker (production-like environment)
make docker-run
```

The API will be available at `http://localhost:8000`

**Test the API:**
```bash
curl http://localhost:8000/
```

### Step 4: Push to GitHub (Triggers CI/CD)

```bash
git push origin main
```

CI/CD will:
- ✅ Run tests automatically
- ✅ Build Docker image in clean Linux environment  
- ✅ Run security scans
- ✅ Report results on GitHub

## Project Structure

```
.
├── Capabilities/
│   ├── app.py                    # Main Chalice application
│   ├── chalicelib/               # Service implementations
│   │   ├── polly_service.py      # Text-to-speech service
│   │   ├── translation_service.py # Translation service
│   │   ├── recognition_service.py # Speech recognition service
│   │   └── storage_service.py    # S3 storage service
│   └── requirements.txt
├── testing/
│   ├── utest_translation.py      # Unit tests
│   └── [service implementations]
├── anmol_filesupload.py          # File upload script
└── Makefile                      # Build automation
```

## AWS Services Used

- **AWS S3**: File storage
- **AWS Translate**: Text translation
- **AWS Polly**: Text-to-speech conversion
- **AWS Rekognition**: Image/speech recognition

## Docker

Build and run the application in a Docker container:

```bash
# Build Docker image (includes running tests)
make docker-build

# Run the Chalice API in Docker with AWS credentials
docker run -it --rm \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=us-east-1 \
  -p 8000:8000 \
  anmol-assignment1:latest
```

The API will be available at `http://localhost:8000`

**Using make:**
```bash
# Run with local AWS credentials
make docker-run
```

## Deploying to Production

### Deploy to AWS Lambda

```bash
cd Capabilities
chalice deploy
```

This will:
- 📦 Package your application
- ☁️ Create AWS Lambda functions
- 🌐 Set up API Gateway endpoints
- 🚀 Deploy to AWS

Chalice will output your API URL. You can then access it from anywhere!

### Before Deploying

1. ✅ Tests pass locally: `make test`
2. ✅ Docker builds locally: `make docker-build`
3. ✅ GitHub Actions CI/CD passes (all checks green)
4. ✅ AWS credentials configured: `aws configure`

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration with:
- Automated test execution
- Code quality checks (pylint, black, isort)
- Security scanning (bandit, safety)
- Multi-stage Docker build (tests run during build)
- Coverage reporting

See `.github/workflows/ci.yml` for workflow configuration.

**How it works:**
1. Push code → GitHub Actions runs automatically
2. Tests fail → Build stops, you fix it
3. Tests pass → Docker image built successfully
4. All checks pass → Ready to deploy

## Make Targets

- `make help` - Display all available targets
- `make install` - Install dependencies
- `make test` - Run tests
- `make test-verbose` - Run tests with verbose output
- `make test-coverage` - Run tests with coverage report
- `make lint` - Run linting checks
- `make format` - Format code with black
- `make clean` - Clean build artifacts
- `make docker-build` - Build Docker image
- `make docker-run` - Run application in Docker

## License

MIT

## Author

Anmol Sagar Shrestha
