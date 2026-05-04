# Stage 1: Test
FROM python:3.11-slim as test

WORKDIR /app

# Accept AWS credentials as build arguments
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION=us-east-1

# Set environment variables for boto3
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_REGION=$AWS_REGION

COPY requirements.txt test-requirements.txt ./
COPY Capabilities/requirements.txt ./Capabilities/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r Capabilities/requirements.txt && \
    pip install --no-cache-dir -r test-requirements.txt

COPY . .

# Run tests - build fails if tests fail
RUN cd testing && python -m pytest utest_translation.py -v

# Stage 2: Production
FROM python:3.11-slim as production

WORKDIR /app

# Only include production dependencies (no test tools)
COPY requirements.txt ./
COPY Capabilities/requirements.txt ./Capabilities/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r Capabilities/requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Default command for production
CMD ["python", "anmol_filesupload.py"]
