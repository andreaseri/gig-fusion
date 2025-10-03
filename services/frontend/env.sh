#!/bin/sh
set -e

TARGET_DIR=/usr/share/nginx/html
PREFIX="ENVSUB_"

echo "Replacing environment placeholders (prefix: $PREFIX) in JS/CSS/HTML files under $TARGET_DIR"

# Loop over env vars starting with the prefix
env | grep "^${PREFIX}" | while IFS='=' read -r key value; do
    echo "  -> substituting $key with $value"

    # Replace across selected file types
    find "$TARGET_DIR" -type f \( -name '*.js' -o -name '*.css' -o -name '*.html' \) \
      -exec sed -i "s|${key}|${value}|g" {} +
done