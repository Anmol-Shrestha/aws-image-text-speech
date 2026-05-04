import boto3
from .aws_config import AWS_REGION


class StorageService:
    def __init__(self, storage_location):
        self.client = boto3.client('s3', region_name=AWS_REGION)
        self.bucket_name = storage_location

    def get_storage_location(self):
        return self.bucket_name

    def upload_file(self, file_bytes, file_name):
        self.client.put_object(Bucket = self.bucket_name,
                               Body = file_bytes,
                               Key = file_name)

        # Generate a signed URL valid for 1 hour
        signed_url = self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_name},
            ExpiresIn=3600
        )

        return {'fileId': file_name,
                'fileUrl': signed_url}
