# Use the latest version of Python 3.10 as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

# Create a new non-root user called "app" with a login shell
RUN useradd -ms /bin/bash app

# Set the working directory to /code for all future commands
WORKDIR /code

# Install necessary Python packages as root before switching to the app user
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY api.py /code/
COPY core /code/core/

# Change ownership of the /code directory to the app user
RUN chown -R app:app /code

# Switch to the app user so that any future commands are run as that user
USER app

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api:app"]
