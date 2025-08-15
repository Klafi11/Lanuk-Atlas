#!/bin/bash

# Script to fill the database

set -e

echo "🗄️  Start filling the database with weather and text data"
echo ""

cd "Lanuk-DB"

poetry env use python3.12
poetry env info
poetry install --no-root
poetry run python main.py

cd ..

echo ""
echo "✅ Database filled with weather and text data"
