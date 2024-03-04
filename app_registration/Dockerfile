FROM tdmx/base:latest

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev libsystemd-dev python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN chown -R appuser:appuser /app

USER appuser

# Setup virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app_registration.py"]