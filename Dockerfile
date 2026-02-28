# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY create_database.py .
COPY create_training_database.py .
COPY train_model.py .
COPY training_dashboard.py .
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create training database at build time
RUN python3 create_training_database.py

# Expose Streamlit port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Start Streamlit app (business database will be created at runtime if needed)
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
