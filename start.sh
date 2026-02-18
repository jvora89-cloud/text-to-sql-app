#!/bin/bash
set -e

echo "Creating database..."
python create_database.py

echo "Starting Streamlit app..."
streamlit run app.py --server.port=7860 --server.address=0.0.0.0
