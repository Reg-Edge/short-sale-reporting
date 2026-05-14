# Short Sales Dashboard — Developer Guide

A step-by-step guide for making changes to the dashboard, testing locally, and deploying to AWS.

---

## One-Time Setup

### Prerequisites

Install these once on your Mac:

| Tool | Install |
|------|---------|
| Node.js 20 | `brew install node@20` |
| Python 3.12 + uv | `brew install uv` |
| Docker Desktop | https://www.docker.com/products/docker-desktop/ |
| AWS CLI | `brew install awscli` |

Verify Node 20 is on your PATH:
```bash
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
node --version   # should print v20.x.x
```

Add that export to your `~/.zshrc` so it persists.

### Get the code

```bash
git clone <repo-url>
cd AWS_Infrastructure/apps/short-sales-dashboard
```

### Install Evidence.dev dependencies (once)

```bash
cd evidence-app
npm install
```

---

## Project Structure

```
apps/short-sales-dashboard/
├── data/
│   └── raw/              ← drop new CSV/Excel files here
├── pipeline/             ← Python: converts raw files → Parquet
├── evidence-app/
│   ├── pages/            ← EDIT THESE to change dashboard content
│   │   ├── index.md      ← Home page (KPI cards)
│   │   ├── exceptions/   ← Exceptions Dashboard
│   │   └── ledger/       ← Ledger Detail drill-through
│   └── sources/short_sales/  ← SQL that reads the Parquet files
└── infrastructure/       ← Terraform (AWS infra — rarely touched)
```

---

## Workflow A — Changing Dashboard Pages (Most Common)

Use this when you want to add/remove charts, change titles, adjust filters, or tweak SQL queries in any of the `.md` pages.

**Edit** any file under `evidence-app/pages/`:

```bash
# Example: open in your editor
code evidence-app/pages/exceptions/index.md
```

**Build and preview:**

```bash
cd evidence-app
PATH="/opt/homebrew/opt/node@20/bin:$PATH" npm run build
PATH="/opt/homebrew/opt/node@20/bin:$PATH" npm run preview
```

The preview command prints a local URL like `http://localhost:4173/short-sales/`. Open it in your browser.

**Iterate:** edit → build → refresh browser. Each build takes ~30 seconds.

> **Note:** Do NOT use `npm run dev`. Use `build + preview` instead — it runs the same path as production.

---

## Workflow B — Refreshing with New Data

Use this when you have new CSV or Excel files from the trading system.

**Step 1 — Drop files into `data/raw/`**

```
data/raw/
├── Multi_Symbol_Intraday_Ledger_Dec2025_FINAL.xlsx   ← intraday ledger
├── ledger_2025-10-26.csv
├── ledger_2025-10-27.csv
└── ...
```

**Step 2 — Convert raw files to Parquet**

```bash
cd pipeline
uv sync          # first time only
uv run python -m short_sales_pipeline.cli convert \
  --raw-dir ../data/raw \
  --out-dir ../data/parquet
```

Expected output: `converted X files → ../data/parquet/`

**Step 3 — Re-run Evidence sources**

```bash
cd ../evidence-app
PATH="/opt/homebrew/opt/node@20/bin:$PATH" npm run sources
```

Expected output: table names + row counts (e.g. `intraday_ledger: 2045 rows`).

**Step 4 — Rebuild and preview**

```bash
PATH="/opt/homebrew/opt/node@20/bin:$PATH" npm run build
PATH="/opt/homebrew/opt/node@20/bin:$PATH" npm run preview
```

---

## Workflow C — Full Docker Test (Before Deploying)

Run this to confirm the dashboard works exactly as it will in AWS.

**Requires:** Docker Desktop must be running.

```bash
cd apps/short-sales-dashboard   # from repo root

docker build -t short-sales-dashboard .
docker run --rm -p 4000:80 short-sales-dashboard
```

Open http://localhost:4000/short-sales/ in your browser.

- Home page should show KPI cards (Records in Ledger, Total Exceptions, Exception %)
- Exceptions page should show charts with data
- Ledger page should show the data table

Once satisfied, press `Ctrl+C` to stop the container.

> **Note:** The Docker build runs the full pipeline inside the container — it converts the raw files in `data/raw/` automatically. No separate pipeline step needed.

---

## Workflow D — Deploy to AWS

**Prerequisites:**
- Docker Desktop running
- AWS CLI configured with profile `re_prabhakaran`
- Docker test (Workflow C) passed

### Step 1 — Log in to ECR

```bash
AWS_PROFILE=re_prabhakaran aws ecr get-login-password \
  --region us-east-1 | \
  docker login --username AWS --password-stdin \
  300553112090.dkr.ecr.us-east-1.amazonaws.com
```

Expected: `Login Succeeded`

### Step 2 — Tag and push the image

```bash
# Tag with a timestamp so you can identify it
TAG=$(date +%Y%m%d-%H%M%S)
ECR=300553112090.dkr.ecr.us-east-1.amazonaws.com/regedge-short-sales

docker tag short-sales-dashboard:latest $ECR:$TAG
docker tag short-sales-dashboard:latest $ECR:latest

docker push $ECR:$TAG
docker push $ECR:latest
```

### Step 3 — Deploy to ECS

```bash
AWS_PROFILE=re_prabhakaran aws ecs update-service \
  --cluster regedge-cloud-service-dev \
  --service regedge-dev-short-sales \
  --force-new-deployment \
  --region us-east-1
```

### Step 4 — Wait for the service to stabilize (~2 minutes)

```bash
AWS_PROFILE=re_prabhakaran aws ecs wait services-stable \
  --cluster regedge-cloud-service-dev \
  --services regedge-dev-short-sales \
  --region us-east-1 && echo "DEPLOYED"
```

### Step 5 — Verify

Open:
```
http://regedge-cloud-services-dev-alb-644193154.us-east-1.elb.amazonaws.com/short-sales/
```

---

## Quick Reference

| Task | Commands |
|------|----------|
| Change a chart or filter | Edit `evidence-app/pages/**/*.md` → `npm run build` → `npm run preview` |
| New data files | Drop in `data/raw/` → pipeline convert → `npm run sources` → `npm run build` |
| Full container test | `docker build -t short-sales-dashboard .` → `docker run -p 4000:80 short-sales-dashboard` |
| Deploy to AWS | ECR login → tag + push → `aws ecs update-service --force-new-deployment` |

---

## Troubleshooting

**Build fails with `node: command not found`**
```bash
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
```

**Pipeline fails with `could not parse '470.0' as dtype i64`**
The CSV has float-formatted integers. This is handled automatically by the pipeline. If it recurs, check that you are running the latest version of `pipeline/src/short_sales_pipeline/convert.py`.

**Dashboard shows grey boxes / "No Records"**
The Parquet files may be missing or sources haven't been re-run. Run `npm run sources` and check the row counts printed — they should be > 0.

**Docker build fails with `BadZipFile`**
You have a `~$*.xlsx` Excel lock file in `data/raw/`. Close Excel and delete the lock file (starts with `~$`), then rebuild.

**ECS deployment fails: `CannotPullContainerError … linux/amd64`**
The image was built for the wrong CPU architecture. Build on your Mac (ARM64) and push — the ECS task definition is already configured for ARM64. Do not add `--platform linux/amd64` to your docker build command.
