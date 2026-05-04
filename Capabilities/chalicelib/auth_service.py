import os
import requests
import jwt
from chalice import UnauthorizedError
from jwt.algorithms import RSAAlgorithm

CLERK_JWKS_URL = os.environ.get('CLERK_JWKS_URL', '')

def get_public_key(token):
    """Fetch the public key from Clerk's JWKS endpoint that matches the token's kid"""
    header = jwt.get_unverified_header(token)
    jwks_response = requests.get(CLERK_JWKS_URL, timeout=5)
    jwks_response.raise_for_status()
    jwks = jwks_response.json()

    for key in jwks['keys']:
        if key['kid'] == header['kid']:
            return RSAAlgorithm.from_jwk(key)

    raise UnauthorizedError("No matching key found in JWKS")

def verify_token(token):
    """Verify a Clerk JWT token and return the decoded payload"""
    try:
        public_key = get_public_key(token)
        return jwt.decode(token, public_key, algorithms=['RS256'])
    except UnauthorizedError:
        raise
    except Exception as e:
        raise UnauthorizedError(f"Invalid or expired token: {str(e)}")
