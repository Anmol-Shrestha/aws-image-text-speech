FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt test-requirements.txt ./
COPY Capabilities/requirements.txt ./Capabilities/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r Capabilities/requirements.txt && \
    pip install --no-cache-dir -r test-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "pytest", "testing/utest_translation.py", "-v"]
