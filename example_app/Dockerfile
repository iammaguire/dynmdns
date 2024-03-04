FROM tdmx/base:latest

# Ensure the home directory is setup properly for appuser
USER root
RUN mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser

WORKDIR /app

# Copy your application files as appuser to ensure correct permissions
COPY --chown=appuser:appuser . /app
COPY --chown=appuser:appuser requirements.txt /app/

# Switch to appuser for subsequent commands
USER appuser

# Ensure the correct virtual environment's pip is used for installing requirements
# The PATH environment should have been set in your base image but reiterating here for clarity
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
CMD ["python", "app.py"]