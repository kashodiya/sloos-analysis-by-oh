#!/bin/bash

# SLOOS Interactive Analysis Application Startup Script

echo "🚀 Starting SLOOS Interactive Analysis Application..."
echo "=================================================="

# Activate UV environment and run Streamlit
cd /home/ec2-user/sloos/sloos-analysis-by-oh

echo "📦 Using UV virtual environment..."
uv run streamlit run app.py --server.port=7251 --server.address=0.0.0.0 --server.headless=true

echo "✅ Application started on port 7251"
