Here’s a well-structured `README.md` file for your project. It includes instructions for cloning the repository, building and running the Docker container, and a clean illustration of the dependencies and calls.

---

 **StackOverflow Crawler with Kafka**

This project is a Python-based application that monitors StackOverflow for new questions tagged with a specific programming language. It uses Kafka for message queuing and Docker for containerization.

---

 **Table of Contents**
1. [Getting Started](getting-started)
   - [Clone the Repository](clone-the-repository)
   - [Install Dependencies](install-dependencies)
2. [Running with Docker](running-with-docker)
   - [Build the Docker Image](build-the-docker-image)
   - [Run the Docker Container](run-the-docker-container)
3. [Project Structure](project-structure)
4. [Dependencies and Workflow](dependencies-and-workflow)
5. [License](license)

---

 **Getting Started**

 **Clone the Repository**
To get started, clone the repository to your local machine:

```bash
git clone https://github.com/mrm68/StackOverFlow_Crawler.git
cd StackOverFlow_Crawler
```

---

 **Install Dependencies**
Install the required Python dependencies:

```bash
pip install -r StackOverFlow_Crawler_Kafka/requirements.txt
```

---

 **Running with Docker**

 **Build the Docker Image**
Navigate to the project root directory and build the Docker image:

```bash
docker build -t stackoverflow-watcher .
```

---

 **Run the Docker Container**
Run the Docker container interactively:

```bash
docker run -it --rm stackoverflow-watcher
```

To persist the `last_seen_id` file outside the container, use a Docker volume:

```bash
mkdir -p ./data
docker run -it --rm -v $(pwd)/data:/app/data stackoverflow-watcher
```

---

 **Project Structure**
```
.
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── StackOverFlow_Crawler_Kafka
    ├── display.py
    ├── main.py
    ├── models.py
    ├── requirements.txt
    ├── scraper.py
    ├── watcher.py
    └── kafka
        ├── producer.py
        └── consumer.py
```

---

 **Dependencies and Workflow**

 **Dependency Graph**
```plaintext
main.py
  │
  └── main()
      │
      └── QuestionWatcher(language, check_interval)
          │
          ├── StackOverflowScraper(language)
          │   ├── fetch_page(page)
          │   ├── parse_page(html)
          │   └── get_questions(stop_condition)
          │
          └── QuestionDisplay
              └── display(questions)
```

 **Workflow**
1. **`main.py`**:
   - Calls `main()` to start the application.
   - Prompts the user for the programming language and check interval.

2. **`QuestionWatcher`**:
   - Initializes with the provided `language` and `check_interval`.
   - Uses `StackOverflowScraper` to fetch and parse questions from StackOverflow.
   - Tracks the last seen question ID using `last_seen_id_<language>.txt`.

3. **`StackOverflowScraper`**:
   - Fetches HTML content from StackOverflow using `fetch_page(page)`.
   - Parses the HTML to extract questions using `parse_page(html)`.
   - Returns a list of `Question` objects using `get_questions(stop_condition)`.

4. **`QuestionDisplay`**:
   - Displays the questions in a formatted way using `display(questions)`.

5. **Kafka Integration**:
   - The `kafka` directory contains `producer.py` and `consumer.py` for sending and receiving messages via Kafka.

---

 **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
