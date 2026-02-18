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

# Expose Streamlit port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Create startup script that initializes database and starts Streamlit
RUN echo '#!/bin/bash\n\
python create_database.py\n\
streamlit run app.py --server.port=7860 --server.address=0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start app
CMD ["/bin/bash", "/app/start.sh"]
