# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY create_database.py .
COPY README.md .
COPY start.sh .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make startup script executable
RUN chmod +x start.sh

# Expose Streamlit port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Start app
CMD ["./start.sh"]
