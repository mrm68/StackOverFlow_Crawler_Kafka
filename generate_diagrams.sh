#!/bin/bash

# Use the OUTPUT_DIR environment variable if provided; default to /app/diagrams.
OUTPUT_DIR=${OUTPUT_DIR:-/app/diagrams}
mkdir -p "$OUTPUT_DIR"

echo "Generating diagrams to $OUTPUT_DIR..."

# Generate targeted diagram: diagram starting from the defined target function.
code2flow \
    ./StackOverFlow_Crawler_Kafka/Crawler/watcher.py \
    ./StackOverFlow_Crawler_Kafka/main.py \
    ./StackOverFlow_Crawler_Kafka/models.py \
    --output "$OUTPUT_DIR/crawler_flow.png" \
    --language py \
    --target-function "QuestionWatcher.start_watching" \
    --downstream-depth 10

# Generate full system diagram from key files.
code2flow \
    ./StackOverFlow_Crawler_Kafka/Crawler/*.py \
    ./StackOverFlow_Crawler_Kafka/main.py \
    ./StackOverFlow_Crawler_Kafka/models.py \
    --output "$OUTPUT_DIR/full_flow.png" \
    --language py

# Generate complete function call hierarchy by scanning the entire repository.
code2flow \
    ./StackOverFlow_Crawler_Kafka/ \
    --output "$OUTPUT_DIR/full_hierarchy.png" \
    --language py

echo "Diagrams generated:"
ls -la "$OUTPUT_DIR"
