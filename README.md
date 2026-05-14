
## Database Setup


1. **Install Docker Desktop**
   ```bash
   https://docs.docker.com/engine/install/
   ```

2. **Start Docker Desktop Engine**

3. **Docker Compose and Pull PostgreSQL**
   ```bash
   docker compose up -d
   docker pull postgres:16   
   ```

4. **Setup Database and Initialize Table Schemas**
   ```bash
   For # macOS/Linux
   docker exec -i ss-pg-1 psql -U postgres -d app -v ON_ERROR_STOP=1 -f - < schema.sql 

   For # Windows 
   Get-Content schema.sql | docker exec -i short_sales-pg-1 psql -U postgres -d app -v ON_ERROR_STOP=1    
   ```
--- 
# Short Sales Dashboard

Open-source recreation of the Power BI "Short Sales Dashboard" using [Evidence.dev](https://docs.evidence.dev) — a code-driven analytics framework built on SvelteKit and DuckDB.

## What It Does

Tracks trading ledger exceptions across intraday and historical date ranges:

- **Home** — KPI cards: Records in Ledger, Total Exceptions, Exception %
- **Exceptions Dashboard** — Treemap + Bar chart of exceptions by SYMBOL and AGG_UNIT, with 4 slicers
- **Exceptions & Ledger** — Full drill-through DataTable with 5 filters

## Data Sources

| File | Table | Notes |
|------|-------|-------|
| `Intraday_Ledger.xlsx` (sheet: FINAL) | `intraday_ledger` | Primary table; derives `IS_EXCEPTION_FLAG` from "Y"/"N" column |
| `ledger_2025-10-29.csv` | `ledger_oct29` | Historical — 15 columns |
| `ledger_2025-10-30.csv` | `ledger_oct30` | Historical — 15 columns |

All source files are converted to **Parquet** by the Python pipeline.

---

## Local Development

### Prerequisites

- Python 3.12+ with [uv](https://github.com/astral-sh/uv)
- Node.js 20+

### Step 1 — Place raw data files

Copy your source files into `data/raw/`:

```
data/raw/
├── ledger_2025-10-29.csv
├── ledger_2025-10-30.csv
└── Multi_Symbol_Intraday_Ledger_Dec2025_FINAL.xlsx
```

### Step 2 — Convert to Parquet

```bash
cd pipeline
uv sync
uv run python -m short_sales_pipeline.cli convert \
  --raw-dir ../data/raw \
  --out-dir ../data/parquet
```

### Step 3 — Run Evidence.dev dev server

```bash
cd evidence-app
npm install
npm run sources   # DuckDB reads Parquet → Evidence internal cache
npm run dev       # http://localhost:3000
```

### Fetch data from S3 (instead of converting locally)

```bash
cd pipeline
uv run python -m short_sales_pipeline.cli fetch \
  --parquet-dir ../data/parquet
```

---

## Docker (full build)

```bash
# From apps/short-sales-dashboard/
docker build -t short-sales .
docker run -p 4000:80 short-sales
# Open http://localhost:4000/short-sales/
```

Or via the root dev script:

```bash
docker compose up --build short-sales
```

---

## Data Refresh Workflow

When new ledger files are available:

1. Place new CSV/Excel files in `data/raw/`
2. Run `pipeline`: `uv run python -m short_sales_pipeline.cli convert-and-upload`
3. Rebuild and redeploy: `./dev deploy short-sales` (from the repo root)

The Docker build re-runs the pipeline and Evidence build automatically, embedding the latest data into the static site.

---

## Deployment

```bash
# From repo root
./dev deploy short-sales
```

This builds a `linux/amd64` image, pushes it to ECR (`regedge-short-sales`), and force-updates the ECS service (`regedge-dev-short-sales`).

The app is served at `https://<alb-dns>/short-sales/`.

### Infrastructure

```bash
cd infrastructure/
terraform init
terraform apply
```

Resources created: ECR repo, ECS task/service, ALB target group + listener rule (priority 140), IAM execution + task roles.
