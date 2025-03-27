#!/bin/bash

# Set output directory (mount this when running)
OUTPUT_DIR=${OUTPUT_DIR:-/app/diagrams}
mkdir -p $OUTPUT_DIR

echo "Generating diagrams to $OUTPUT_DIR..."

# Generate targeted diagram
code2flow \
    ./StackOverFlow_Crawler_Kafka/Crawler/watcher.py \
    ./StackOverFlow_Crawler_Kafka/main.py \
    ./StackOverFlow_Crawler_Kafka/models.py \
    --output $OUTPUT_DIR/crawler_flow.png \
    --language py \
    --target-function "QuestionWatcher.start_watching" \
    --downstream-depth 3

# Generate full system diagram
code2flow \
    ./StackOverFlow_Crawler_Kafka/Crawler/*.py \
    ./StackOverFlow_Crawler_Kafka/main.py \
    ./StackOverFlow_Crawler_Kafka/models.py \
    --output $OUTPUT_DIR/full_flow.png \
    --language py

echo "Diagrams generated:"
ls -la $OUTPUT_DIR