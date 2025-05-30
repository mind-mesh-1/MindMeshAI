#!/bin/zsh

# Build the frontend with limited memory usage
echo "Building frontend..."
npm install
NODE_OPTIONS="--max_old_space_size=1024" npm run build
npm start &

# Start FastAPI backend with Uvicorn in production mode
echo "Starting FastAPI backend..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4