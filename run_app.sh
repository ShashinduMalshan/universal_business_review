#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================================="
echo " Starting Universal Business Review Analyzer (Full-Stack Platform)"
echo "========================================================================="

# Ensure virtual environment exists
if [ ! -d "$DIR/venv" ]; then
    echo "[INFO] Creating Python virtual environment in $DIR/venv ..."
    python3 -m venv "$DIR/venv"
fi

# Ensure dependencies are installed
if [ ! -f "$DIR/venv/bin/uvicorn" ]; then
    echo "[INFO] Installing required dependencies (fastapi, uvicorn, scikit-learn, etc.)..."
    "$DIR/venv/bin/pip" install --upgrade pip
    "$DIR/venv/bin/pip" install -r "$DIR/backend/requirements.txt"
fi

echo " Web Dashboard  : http://127.0.0.1:8000"
echo " REST API Docs  : http://127.0.0.1:8000/docs"
echo " Health Status  : http://127.0.0.1:8000/api/health"
echo "========================================================================="

export PYTHONPATH="$DIR:$PYTHONPATH"
"$DIR/venv/bin/uvicorn" backend.main:app --host 127.0.0.1 --port 8000 --reload

