import os
import uuid

import boto3
from chalice import BadRequestError
from .aws_config import AWS_REGION

# Formats Rekognition's DetectText accepts
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


class StorageService:
    def __init__(self, storage_location):
        self.client = boto3.client('s3', region_name=AWS_REGION)
        self.bucket_name = storage_location

    def get_storage_location(self):
        return self.bucket_name

    def make_key(self, file_name):
        """Build a safe S3 key from the user's file name, so the user's name never reaches S3 or the URL"""
        extension = os.path.splitext(file_name)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise BadRequestError(f"Unsupported file type '{extension}'. Use JPG or PNG.")
        return f"{uuid.uuid4().hex}{extension}"

    def upload_file(self, file_bytes, file_name):
        key = self.make_key(file_name)

        self.client.put_object(Bucket = self.bucket_name,
                               Body = file_bytes,
                               Key = key)

        # Generate a signed URL valid for 1 hour
        signed_url = self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key},
            ExpiresIn=3600
        )

        return {'fileId': key,
                'fileUrl': signed_url}
