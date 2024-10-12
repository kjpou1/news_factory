# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /usr/src/app

# Step 3: Install required system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    wget \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the current directory contents into the container at /usr/src/app
COPY . .

# Step 5: Ensure the resources folder is copied
COPY resources ./resources

# Step 6: Install the dependencies specified in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Install Playwright once and cache it
RUN pip install --no-cache-dir playwright && playwright install chromium

# Expose the data directory for external mapping
VOLUME [ "/app/data" ]

# Step 8: Define environment variables (optional)
#ENV OUTPUT_FOLDER=/usr/src/app/data_files

# Step 9: Set the command to run your Python script
CMD ["python", "scheduler_script.py"]
