FROM tdmx/base:latest
WORKDIR /app
COPY . /app
COPY requirements.txt /app/
USER appuser
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "app.py"]