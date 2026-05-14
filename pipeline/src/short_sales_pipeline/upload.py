"""Upload Parquet files to S3 stage bucket."""

from pathlib import Path

import boto3


STAGE_BUCKET = "regedge-cloud-services-dev-stage"
S3_PREFIX = "short-sales/parquet"


def upload_parquet(parquet_dir: Path, bucket: str = STAGE_BUCKET, prefix: str = S3_PREFIX) -> None:
    """Upload all Parquet files from parquet_dir to S3."""
    s3 = boto3.client("s3")
    files = list(parquet_dir.glob("*.parquet"))
    if not files:
        print(f"No Parquet files found in {parquet_dir}")
        return

    for f in files:
        key = f"{prefix}/{f.name}"
        print(f"  Uploading {f.name} → s3://{bucket}/{key}")
        s3.upload_file(str(f), bucket, key)

    print(f"Uploaded {len(files)} file(s) to s3://{bucket}/{prefix}/")


def download_parquet(parquet_dir: Path, bucket: str = STAGE_BUCKET, prefix: str = S3_PREFIX) -> None:
    """Download Parquet files from S3 to parquet_dir (for local dev)."""
    s3 = boto3.client("s3")
    parquet_dir.mkdir(parents=True, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix + "/")
    downloaded = 0
    for page in pages:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".parquet"):
                continue
            filename = Path(key).name
            dst = parquet_dir / filename
            print(f"  Downloading s3://{bucket}/{key} → {filename}")
            s3.download_file(bucket, key, str(dst))
            downloaded += 1

    print(f"Downloaded {downloaded} file(s) to {parquet_dir}")
