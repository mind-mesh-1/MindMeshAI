#!/bin/zsh

echo "Building frontend..."
npm install
NODE_OPTIONS="--max_old_space_size=768" cpulimit --limit 70 -- npm run build -- --no-lint --verbose

npm start &

echo "Starting FastAPI backend..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4