#!/bin/zsh
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
ARCHIVE_NAME="nenets_verb_lemmatizer_submission_$(date +%Y%m%d).zip"
ARCHIVE_PATH="$DIST_DIR/$ARCHIVE_NAME"

mkdir -p "$DIST_DIR"
rm -f "$ARCHIVE_PATH"

cd "$ROOT_DIR"
zip -r "$ARCHIVE_PATH" \
  manage.py \
  config \
  lemmatizer_app \
  README.md \
  requirements.txt \
  registration_package \
  docs \
  legacy \
  .gitignore \
  -x "*.pyc" "*/__pycache__/*" "*.sqlite3" "dist/*" "*/.DS_Store" "*/.git/*"

echo "$ARCHIVE_PATH"
