# =============================================================================
# Stage 1: Build Evidence.dev static site
# =============================================================================
FROM node:20-bookworm-slim AS builder

WORKDIR /app

# Install dependencies first for layer caching
COPY evidence-app/package*.json ./
RUN npm ci

# Copy source files (pages, sources, config) — node_modules excluded via .dockerignore
COPY evidence-app/evidence.config.yaml ./
COPY evidence-app/sources ./sources
COPY evidence-app/pages ./pages

# Use pre-built Parquet files directly (bypasses polars pipeline stage)
COPY data/parquet/ /parquet/

# The source SQL files reference ${data_dir} which is supplied via EVIDENCE_VAR__
ENV EVIDENCE_VAR__data_dir=/parquet/

RUN npm run sources && \
    EVIDENCE_BUILD_DIR=./build/short-sales npm run build

# =============================================================================
# Stage 3: Serve pre-built static files with Nginx
# =============================================================================
FROM nginx:alpine

COPY --from=builder /app/build/short-sales /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
