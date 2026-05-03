import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3 = boto3.client("s3")

DEST_BUCKET = "machinelearning21"   # destination bucket
DEST_PREFIX = "resized/"            # folder in destination

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

def lambda_handler(event, context):
    for record in event["Records"]:
        src_bucket = record["s3"]["bucket"]["name"]
        src_key = unquote_plus(record["s3"]["object"]["key"])

        # Optional: only process files under original/
        if not src_key.startswith("original/"):
            print(f"Skipping (not in original/): {src_key}")
            continue

        tmpkey = src_key.replace("/", "")
        download_path = f"/tmp/{uuid.uuid4()}-{tmpkey}"
        upload_path = f"/tmp/resized-{tmpkey}"

        s3.download_file(src_bucket, src_key, download_path)
        resize_image(download_path, upload_path)

        out_key = DEST_PREFIX + os.path.basename(src_key)
        s3.upload_file(upload_path, DEST_BUCKET, out_key)

        print(f"Uploaded thumbnail to s3://{DEST_BUCKET}/{out_key}")

    return {"statusCode": 200, "body": "OK"}
