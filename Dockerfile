# 1. Start with a lightweight Python Linux image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your script and the dummy file into the container
COPY main.py .
COPY dummy_diff.txt .

# 5. Define the command to run when the container starts
ENTRYPOINT ["python", "/app/main.py"]