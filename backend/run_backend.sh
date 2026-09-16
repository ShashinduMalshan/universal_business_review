#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$( cd "$DIR/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "================================================================="
echo " Starting Universal Business Review Analyzer Backend Server"
echo "================================================================="

# Ensure virtual environment exists
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "[INFO] Creating Python virtual environment in $ROOT_DIR/venv ..."
    python3 -m venv "$ROOT_DIR/venv"
fi

# Ensure dependencies are installed
if [ ! -f "$ROOT_DIR/venv/bin/uvicorn" ]; then
    echo "[INFO] Installing required dependencies (fastapi, uvicorn, scikit-learn, etc.)..."
    "$ROOT_DIR/venv/bin/pip" install --upgrade pip
    "$ROOT_DIR/venv/bin/pip" install -r "$DIR/requirements.txt"
fi

echo " Web Dashboard  : http://127.0.0.1:8000"
echo " REST API Docs  : http://127.0.0.1:8000/docs"
echo " Health Status  : http://127.0.0.1:8000/api/health"
echo "================================================================="

export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"
"$ROOT_DIR/venv/bin/uvicorn" main:app --host 127.0.0.1 --port 8000 --reload

