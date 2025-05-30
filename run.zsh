#!/bin/zsh

# Build the frontend
echo "Building frontend..."
npm install
npm run build
npm start &


# Start FastAPI backend with Uvicorn in production mode
echo "Starting FastAPI backend..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4