#!/bin/bash
#
# Update SLOOS Data Script
# Downloads the latest real SLOOS data from FRED and updates the database
#

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                     SLOOS DATA UPDATE SCRIPT                                 ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "📥 Downloading latest SLOOS data from Federal Reserve (FRED)..."
echo ""

uv run python download_real_sloos_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║                          ✅ UPDATE SUCCESSFUL                                ║"
    echo "║                                                                              ║"
    echo "║  The database has been updated with the latest real SLOOS data from FRED.   ║"
    echo "║  The application will now use real Federal Reserve data.                    ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║                          ❌ UPDATE FAILED                                    ║"
    echo "║                                                                              ║"
    echo "║  There was an error downloading or loading the SLOOS data.                  ║"
    echo "║  Please check the error messages above.                                     ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    exit 1
fi
