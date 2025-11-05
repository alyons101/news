#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/.venv"

command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required to run the backend." >&2
  exit 1
}
command -v npm >/dev/null 2>&1 || {
  echo "npm is required to run the frontend." >&2
  exit 1
}

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment for the backend..."
  python3 -m venv "$VENV_DIR"
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip
  pip install -r "$BACKEND_DIR/requirements.txt"
  deactivate
fi

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  echo "Installing frontend dependencies..."
  (cd "$FRONTEND_DIR" && npm install)
fi

echo "Starting backend on http://127.0.0.1:8000 ..."
(
  source "$VENV_DIR/bin/activate"
  cd "$BACKEND_DIR"
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!

trap 'kill $BACKEND_PID $FRONTEND_PID 2>/dev/null' EXIT

sleep 2

echo "Starting frontend on http://127.0.0.1:5173 ..."
(
  cd "$FRONTEND_DIR"
  npm run dev -- --host 0.0.0.0 --port 5173
) &
FRONTEND_PID=$!

wait
