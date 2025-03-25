FROM python:3.9-slim

# Install system dependencies for graphviz
RUN apt-get update && apt-get install -y \    
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY StackOverFlow_Crawler_Kafka/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt code2flow

# Copy all source code
COPY StackOverFlow_Crawler_Kafka/ .

# Add diagram generation script
COPY generate_diagrams.sh .
RUN chmod +x generate_diagrams.sh

CMD ["sh", "-c", "./generate_diagrams.sh && python main.py"]