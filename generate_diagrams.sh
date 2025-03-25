#!/bin/bash

mkdir -p /app/diagrams

# Generate diagram starting from main entry point
code2flow \
    Crawler/watcher.py main.py models.py \
    --output /app/diagrams/crawler_flow.png \
    --language py \
    --target-function "QuestionWatcher.start_watching"

# Alternative simplified version without depth
code2flow \
    Crawler/*.py main.py models.py \
    --output /app/diagrams/full_flow.png \
    --language py

echo "Diagrams generated at:"
ls -la /app/diagrams/