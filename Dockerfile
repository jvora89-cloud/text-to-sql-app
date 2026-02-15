# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY create_database.py .
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create database
RUN python create_database.py

# Expose Streamlit port
EXPOSE 7860

# Start Ollama service and pull model, then run Streamlit
CMD ollama serve & \
    sleep 5 && \
    ollama pull llama3 && \
    streamlit run app.py --server.port=7860 --server.address=0.0.0.0
