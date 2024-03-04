FROM tdmx/base:latest
USER root
RUN apt-get update && apt-get install -y \
    libsystemd-dev \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* 
WORKDIR /app
USER appuser
COPY requirements.txt ./
RUN pip install --user -r requirements.txt
COPY --chown=appuser:appuser . .
CMD ["python", "./mdns_broadcaster.py"]