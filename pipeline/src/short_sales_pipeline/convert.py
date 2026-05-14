"""Convert CSV and Excel source files to Parquet format."""

from pathlib import Path

import polars as pl


LEDGER_CSV_SCHEMA = {
    "SOURCESYSTEM": pl.Utf8,
    "TYPE": pl.Utf8,
    "TIMESTAMP": pl.Utf8,
    "AGGREGATION_UNIT": pl.Utf8,
    "SYMBOL": pl.Utf8,
    "SIDE": pl.Utf8,
    "QUANTITY": pl.Float64,
    "BOOK": pl.Float64,
    "SOD": pl.Float64,
    "CURR_POSITION": pl.Float64,
    "UNIQUEID": pl.Utf8,
    "BUSINESS_DATE": pl.Utf8,
    "PREV_TIMESTAMP": pl.Utf8,
    "NEXT_TIMESTAMP": pl.Utf8,
    "IS_EXCEPTION": pl.Float64,
}

_INT_COLS = ("QUANTITY", "BOOK", "SOD", "CURR_POSITION", "IS_EXCEPTION")


def convert_ledger_csv(src: Path, dst: Path) -> None:
    """Convert a ledger CSV file to Parquet."""
    df = pl.read_csv(src, schema_overrides=LEDGER_CSV_SCHEMA, try_parse_dates=False)
    # Cast float-formatted integers (e.g. "470.0") to Int64
    for col in _INT_COLS:
        if col in df.columns:
            df = df.with_columns(pl.col(col).cast(pl.Int64))
    # Parse timestamp columns from string to datetime
    for col in ("TIMESTAMP", "PREV_TIMESTAMP", "NEXT_TIMESTAMP"):
        if col in df.columns:
            df = df.with_columns(
                pl.col(col).str.to_datetime(format=None, strict=False)
            )
    df.write_parquet(dst)
    print(f"  {src.name} → {dst.name} ({len(df):,} rows)")


def convert_intraday_excel(src: Path, dst: Path) -> None:
    """Convert Intraday_Ledger Excel file to Parquet, adding derived columns."""
    df = pl.read_excel(src, sheet_name="FINAL", engine="openpyxl")

    # Derive IS_EXCEPTION_FLAG from text "Y"/"N" column
    if "IS_EXCEPTION" in df.columns:
        df = df.with_columns(
            pl.when(pl.col("IS_EXCEPTION").cast(pl.Utf8).str.strip_chars() == "Y")
            .then(pl.lit(1))
            .otherwise(pl.lit(0))
            .cast(pl.Int64)
            .alias("IS_EXCEPTION_FLAG")
        )

    # Row_Highlight mirrors IS_EXCEPTION_FLAG
    df = df.with_columns(pl.col("IS_EXCEPTION_FLAG").alias("ROW_HIGHLIGHT"))

    df.write_parquet(dst)
    print(f"  {src.name} → {dst.name} ({len(df):,} rows)")


def convert_all(raw_dir: Path, out_dir: Path) -> None:
    """Convert all source files in raw_dir to Parquet in out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Ledger CSV files
    for csv_file in sorted(raw_dir.glob("ledger_*.csv")):
        out_name = csv_file.stem.lower().replace("-", "_") + ".parquet"
        convert_ledger_csv(csv_file, out_dir / out_name)

    # Intraday Ledger Excel
    for xlsx_file in raw_dir.glob("*.xlsx"):
        convert_intraday_excel(xlsx_file, out_dir / "intraday_ledger.parquet")
