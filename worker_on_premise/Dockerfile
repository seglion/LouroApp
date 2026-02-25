# Build stage
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

# Install build dependencies for geospatial libraries (Fiona/GDAL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim-bookworm

# Install runtime dependencies for GDAL/Fiona
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (Security Hardening)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy app source code, setting ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user (Security Hardening)
USER appuser

# Define volume for persistent storage (Downloads and local SQLite DB)
VOLUME ["/app/data"]

# Entrypoint script
CMD ["python", "main.py"]
