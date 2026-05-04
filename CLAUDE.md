# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pictorial Translate** is a cloud-native application that orchestrates AWS services to upload images, detect text using Rekognition, and translate the detected text to English using Translate. The app features:
- **Frontend**: Static HTML/JS hosted on AWS Amplify
- **Backend**: Python Chalice serverless API on AWS Lambda
- **Authentication**: Clerk OAuth (added May 2026) gates both API endpoints
- **AWS Services**: S3 (storage), Rekognition (text detection), Translate (translation), Polly (text-to-speech)

## Architecture

```
Browser (Clerk Login) → Amplify Frontend (HTML/JS) → API Gateway → Lambda (Chalice)
                                                            ↓
                                    S3 + Rekognition + Translate + Polly
```

**Key endpoints (both require Clerk JWT token):**
- `POST /images` — Upload image to S3, returns fileId and signed URL
- `POST /images/{image_id}/translate-text` — Detect text via Rekognition, translate to English

**Authentication flow (added May 2026):**
1. Frontend loads Clerk JS SDK from CDN
2. User clicks "Sign In" → redirected to Clerk login page
3. After sign-in, frontend retrieves JWT token via `window.Clerk.session.getToken()`
4. All API calls attach token as `Authorization: Bearer {token}` header
5. Backend verifies JWT signature against Clerk's JWKS endpoint
6. Invalid/missing tokens return 401 Unauthorized

## Development

### Install dependencies
```bash
cd Capabilities
pip install -r requirements.txt
```

### Local testing
```bash
# Run tests
make test

# Start Chalice dev server
chalice local
```

### Frontend testing
```bash
cd website
python -m http.server 8080
# Open http://localhost:8080 → Sign in via Clerk (uses test keys)
```

## Backend Code Structure

**Chalice app layout** (`Capabilities/`):
- `app.py` — Main routes with `@require_auth` decorator applied to both endpoints
- `chalicelib/auth_service.py` — JWT verification (fetches Clerk's JWKS, validates RS256 signature)
- `chalicelib/storage_service.py` — S3 upload wrapper
- `chalicelib/recognition_service.py` — Rekognition text detection
- `chalicelib/translation_service.py` — Translate service
- `.chalice/config.json` — Includes `CLERK_JWKS_URL` env var pointing to Clerk's JWKS endpoint
- `requirements.txt` — Includes PyJWT, cryptography, requests (added for Clerk)

**Authentication decorator** (app.py):
```python
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = app.current_request.headers.get('authorization', '')
        if not auth_header.startswith('Bearer '):
            raise UnauthorizedError("Missing or invalid authorization token")
        token = auth_header[7:]
        auth_service.verify_token(token)  # Raises UnauthorizedError if invalid
        return func(*args, **kwargs)
    return wrapper
```

Applied to: `upload_image()` and `translate_image_text()`.

## Frontend Code Structure

**Static HTML/JS** (`website/`):
- `index.html` — Includes Clerk script tag, Sign In button, app content (hidden until authenticated)
- `scripts.js` — Clerk initialization, token retrieval, API calls with Bearer token

**Clerk integration** (scripts.js):
- `initClerk()` — Loads Clerk JS SDK, sets up auth UI
- `getAuthToken()` — Returns JWT token from current session
- Both `uploadImage()` and `translateImage()` attach token to fetch headers

**Key change from pre-auth**: All `fetch()` calls now include:
```javascript
'Authorization': `Bearer ${token}`
```

## Deployment

### Stages
- **`dev` stage** (production): API Gateway endpoint `https://v9c90wf7fj.execute-api.us-east-1.amazonaws.com/api/` with Clerk auth required
- Previous `test-auth` stage deleted after promotion to production

### Deploy backend changes
```bash
cd Capabilities
chalice deploy --stage dev
```

### Deploy frontend changes
Push to `main` branch → Amplify auto-builds and redeploys to its own URL.

## Clerk Configuration

**Test keys** (development):
- Publishable Key: `pk_test_ZXhvdGljLXNjdWxwaW4tOTUuY2xlcmsuYWNjb3VudHMuZGV2JA`
- Frontend API URL: `https://exotic-sculpin-95.clerk.accounts.dev`
- JWKS URL (in config.json): `https://exotic-sculpin-95.clerk.accounts.dev/.well-known/jwks.json`

**Switching to live Clerk keys** (production upgrade):
1. Go to Clerk dashboard → API Keys → switch to "Live"
2. Update `data-clerk-publishable-key` in `index.html`
3. Update `CLERK_JWKS_URL` in `.chalice/config.json` to your live domain
4. Redeploy both frontend and backend

## Common Tasks

### Add a new API endpoint (with auth)
1. Add route in `app.py` with `@require_auth` decorator
2. Auth verification is automatic; request body available via `app.current_request.raw_body`

### Test endpoint without token (local)
```bash
curl -X POST http://localhost:8000/images \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.jpg","filebytes":"..."}'
# Should get 401 Unauthorized
```

### Test endpoint with token (local)
1. Open http://localhost:8080 in browser
2. Sign in via Clerk (uses test keys)
3. Open DevTools Network tab, upload an image
4. Inspect the `/images` request → verify `Authorization: Bearer ...` header is present

### Deploy after code changes
```bash
# Backend
cd Capabilities && chalice deploy --stage dev

# Frontend
git push origin main  # Amplify auto-deploys
```

## Known Limitations & Future Work

- **Rate limiting**: Currently relies on Clerk tracking users; AWS API Gateway throttling not yet configured per-user
- **CORS**: Currently allows all origins (`cors=True`); consider restricting to specific Amplify domain in production
- **Error messages**: 401 response body could be more detailed (planned enhancement)

## Key Files Modified (May 2026 - Clerk Auth)

- `Capabilities/app.py` — Added `@require_auth` decorator and imports
- `Capabilities/requirements.txt` — Added PyJWT, cryptography, requests
- `Capabilities/chalicelib/auth_service.py` — New file for JWT verification
- `Capabilities/.chalice/config.json` — Added `CLERK_JWKS_URL` env var
- `website/index.html` — Added Clerk script tag, Sign In/Out UI
- `website/scripts.js` — Added Clerk initialization, token retrieval in API calls

See git commits `5846f9f` (Clerk auth implementation) and `eaaac30` (promotion to production) for full changes.
