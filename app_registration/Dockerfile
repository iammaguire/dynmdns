FROM tdmx/base:latest
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev libsystemd-dev && \
    rm -rf /var/lib/apt/lists/*
USER appuser
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --user -r requirements.txt
USER root
RUN apt-get purge -y --auto-remove gcc libc6-dev
USER appuser

CMD ["python", "app_registration.py"]