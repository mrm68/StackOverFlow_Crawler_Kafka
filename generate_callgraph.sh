#!/bin/bash

# Set output directory (default to /app/diagrams if not provided via env)
OUTPUT_DIR=${OUTPUT_DIR:-/app/diagrams}
mkdir -p "$OUTPUT_DIR"

echo "Generating full call graph using pyan3..."

# Find all Python files and feed them into pyan3
find ./StackOverFlow_Crawler_Kafka -name "*.py" | xargs pyan3 --dot --no-defines > "$OUTPUT_DIR/full_callgraph.dot"

# Convert the DOT file to a PNG using Graphviz
dot -Tpng "$OUTPUT_DIR/full_callgraph.dot" -o "$OUTPUT_DIR/full_callgraph.png"

echo "Call graph generated at $OUTPUT_DIR:"
ls -la "$OUTPUT_DIR"
