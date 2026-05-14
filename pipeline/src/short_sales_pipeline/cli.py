"""CLI entry point for the short-sales pipeline."""

from pathlib import Path

import click

from .convert import convert_all
from .upload import upload_parquet, download_parquet, STAGE_BUCKET, S3_PREFIX


@click.group()
def main():
    """Short Sales Dashboard data pipeline."""


@main.command()
@click.option("--raw-dir", default="./data/raw", show_default=True, help="Directory with source CSV/Excel files")
@click.option("--out-dir", default="./data/parquet", show_default=True, help="Output directory for Parquet files")
def convert(raw_dir, out_dir):
    """Convert CSV and Excel source files to Parquet."""
    raw = Path(raw_dir)
    out = Path(out_dir)
    if not raw.exists():
        raise click.ClickException(f"Raw directory not found: {raw}")
    print(f"Converting files from {raw} → {out}")
    convert_all(raw, out)
    print("Done.")


@main.command()
@click.option("--parquet-dir", default="./data/parquet", show_default=True, help="Directory with Parquet files")
@click.option("--bucket", default=STAGE_BUCKET, show_default=True)
@click.option("--prefix", default=S3_PREFIX, show_default=True)
def upload(parquet_dir, bucket, prefix):
    """Upload Parquet files to S3 stage bucket."""
    print(f"Uploading from {parquet_dir} → s3://{bucket}/{prefix}/")
    upload_parquet(Path(parquet_dir), bucket=bucket, prefix=prefix)


@main.command("convert-and-upload")
@click.option("--raw-dir", default="./data/raw", show_default=True)
@click.option("--parquet-dir", default="./data/parquet", show_default=True)
@click.option("--bucket", default=STAGE_BUCKET, show_default=True)
@click.option("--prefix", default=S3_PREFIX, show_default=True)
def convert_and_upload(raw_dir, parquet_dir, bucket, prefix):
    """Convert source files to Parquet and upload to S3."""
    raw = Path(raw_dir)
    out = Path(parquet_dir)
    if not raw.exists():
        raise click.ClickException(f"Raw directory not found: {raw}")
    print("Step 1: Converting...")
    convert_all(raw, out)
    print("Step 2: Uploading...")
    upload_parquet(out, bucket=bucket, prefix=prefix)
    print("Done.")


@main.command("fetch")
@click.option("--parquet-dir", default="./data/parquet", show_default=True)
@click.option("--bucket", default=STAGE_BUCKET, show_default=True)
@click.option("--prefix", default=S3_PREFIX, show_default=True)
def fetch(parquet_dir, bucket, prefix):
    """Download Parquet files from S3 for local development."""
    print(f"Fetching from s3://{bucket}/{prefix}/ → {parquet_dir}")
    download_parquet(Path(parquet_dir), bucket=bucket, prefix=prefix)


if __name__ == "__main__":
    main()
