#!/bin/zsh

# Build the frontend with stricter memory limits and no linting
echo "Building frontend..."
npm install
NODE_OPTIONS="--max_old_space_size=768" npm run build -- --no-lint
npm start &

# Start FastAPI backend with Uvicorn in production mode
echo "Starting FastAPI backend..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4