# Use an official Python 3.12 image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add the Python script(s) to the Docker image
WORKDIR /app
COPY . /app

# Give execute permissions to the entrypoint (if needed)
RUN chmod +x ./entrypoint.sh

# Define the entrypoint to run the Python script
ENTRYPOINT ["./entrypoint.sh"]
