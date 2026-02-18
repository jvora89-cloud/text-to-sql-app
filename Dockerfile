# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY create_database.py .
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create database at runtime
RUN python create_database.py

# Expose Streamlit port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
