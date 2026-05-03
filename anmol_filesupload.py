"""
anmol_filesupload.py
Exercise #1 - Upload files to S3 using boto3
Student: Anmol
"""

import boto3
import logging
import time
from botocore.exceptions import ClientError

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s"
)
logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────────
BUCKET_NAME = "contentcen301364068.aws.ai"          # <-- replace with your S3 bucket name
FILES = ["anmol1.txt", "anmol2.txt", "anmol3.txt"]


def upload_files_to_s3(bucket_name: str, file_list: list) -> None:

    s3_client = boto3.client("s3")

    # Record overall start time
    overall_start = time.time()
    logger.info("=== Upload process started ===")
    logger.info("Start time : %.4f seconds (epoch)", overall_start)

    for file_name in file_list:
        try:
            logger.info("Uploading '%s' to bucket '%s' ...", file_name, bucket_name)

            file_start = time.time()

            # Upload the file (key in S3 == file_name, no sub-folder)
            s3_client.upload_file(
                Filename=file_name,
                Bucket=bucket_name,
                Key=file_name
            )

            file_end = time.time()
            logger.info(
                "  ✓ '%s' uploaded successfully in %.3f s",
                file_name,
                file_end - file_start
            )

        except FileNotFoundError:
            # Local file does not exist
            logger.error(
                "  ✗ File '%s' not found locally – skipping.", file_name
            )

        except ClientError as e:
            # boto3 / AWS-level error (permissions, bucket not found, etc.)
            error_code = e.response["Error"]["Code"]
            error_msg  = e.response["Error"]["Message"]
            logger.error(
                "  ✗ ClientError uploading '%s': [%s] %s",
                file_name, error_code, error_msg
            )

        except Exception as e:
            # Catch-all for any unexpected errors
            logger.exception("  ✗ Unexpected error uploading '%s': %s", file_name, e)

    # Record overall end time
    overall_end = time.time()
    logger.info("=== Upload process finished ===")
    logger.info("End time   : %.4f seconds (epoch)", overall_end)
    logger.info("Total time : %.3f seconds", overall_end - overall_start)


if __name__ == "__main__":
    upload_files_to_s3(BUCKET_NAME, FILES)
