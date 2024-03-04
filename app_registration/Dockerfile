FROM python:3.9-slim
WORKDIR /app
COPY . /app/app_registration
COPY ../mdns_registrar /app/mdns_registrar
RUN pip install --no-cache-dir ./mdns_registrar
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./app_registration.py"]