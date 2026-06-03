#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo "  Markdown to PDF"
echo "========================================"
echo ""

# find Python
PYTHON=""
for cmd in python3 python py; do
    if command -v "$cmd" &> /dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[X] Python not found. Please install Python 3.8+"
    echo "    macOS: brew install python3"
    echo "    Linux: sudo apt install python3 python3-pip"
    read -p "Press Enter to exit..." dummy
    exit 1
fi

echo "Python: $PYTHON"
echo ""

# install deps
echo "[1/2] Checking dependencies..."
$PYTHON -c "import markdown" 2>/dev/null || {
    echo "Installing..."
    $PYTHON -m pip install -r requirements.txt -q
}
echo "Done."

# convert
echo ""
echo "[2/2] Converting..."
echo ""
$PYTHON md2pdf.py

echo ""
echo "========================================"
read -p "Press Enter to exit..." dummy
