
 **StackOverflow Crawler with Kafka**

This project is a Python-based application that monitors StackOverflow for new questions tagged with a specific programming language. It uses Kafka for message queuing and Docker for containerization. The project leverages **Pydantic** for robust data modeling, validation, and serialization.

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
   - [Dependency Graph](dependency-graph)
   - [Workflow](workflow)
   - [Pydantic Improvements](pydantic-improvements)
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

---

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

```
[Start Docker Container]
│
├──> 1. Docker Setup
│      │
│      ├── Installs Python 3.9
│      ├── Copies requirements.txt
│      └── Runs pip install
│
├──> 2. Run main.py
│      │
│      ├──> User Input Phase
│      │      │
│      │      ├── Ask for language (e.g., "python")
│      │      └── Ask for check interval (default 60s)
│      │
│      └──> Initialize QuestionWatcher
│             │
│             └──> Creates StackOverflowScraper
│                    │
│                    ├──> Creates Fetcher (Strategy Pattern)
│                    └──> Creates QuestionParser (Template Method)
│
├──> 3. Watcher Start
│      │
│      ├──> check_new_questions() [First Run]
│      │      │
│      │      ├──> scraper.get_questions()
│      │      │      │
│      │      │      ├──> fetcher.fetch(page 1)
│      │      │      │      │
│      │      │      │      ├── Try 3 times
│      │      │      │      └── Return HTML or None
│      │      │      │
│      │      │      └──> parser.parse(HTML)
│      │      │             │
│      │      │             ├── Extract title
│      │      │             ├── Extract votes
│      │      │             ├── Extract answers
│      │      │             └── Create Question objects
│      │      │
│      │      └──> Compare IDs with last_seen_id
│      │
│      └──> Continuous Loop
│             │
│             ├── Sleep for check_interval
│             └── Repeat check_new_questions()
│
├──> 4. Display Flow (When New Questions Found)
│      │
│      ├──> QuestionDisplay.display()
│      │      │
│      │      ├── Clean excerpt text
│      │      ├── Format with emojis
│      │      └── Print to console
│      │
│      └──> Update last_seen_id file
│
├──> 5. Error Handling
│      │
│      ├── Fetch errors → 3 retries
│      ├── Parse errors → Skip question
│      └── KeyboardInterrupt → Graceful exit
│
└──> [Loop Until CTRL+C]
       │
       └──> Watcher keeps checking every N seconds
              │
              ├── New questions → Show notification
              └── No changes → Show status message
```

# **Key Process Relationships:**

1. **Watcher (Observer) Controls Flow**
   - Initializes Scraper (Facade)
   - Calls: scraper.get_questions() → parser.parse() → fetcher.fetch()

2. **Scraper Orchestration**
   - 1 scraper → 1 fetcher + 1 parser
   - Handles pagination automatically

3. **Data Transformation Chain**
   HTML → BeautifulSoup → Question objects → Formatted display

4. **State Management**
   - last_seen_id file persists between runs
   - Auto-saves after each check

 Critical Path Example:

User Input "python" → Watcher Initialized → First Scrape → Display Results → Sleep 60s → Repeat...

 Design Pattern Execution Flow:

1. **Strategy Pattern (Fetcher)**
   - Scraper → Fetcher.fetch()
   - Can swap HTTP libraries without changing core logic

2. **Template Method (Parser)**
   - parse() → _parse_question() → _extract_title()/_extract_votes()
   - Fixed process with customizable steps

3. **Facade Pattern (Scraper)**
   - Simple get_questions() hides:
     - Pagination
     - HTML fetching
     - Data parsing

4. **Observer Pattern (Watcher)**
   - Continuous monitoring loop
   - State comparison (new vs old IDs)

 Overload Protection:

1. Fetcher: 3 retries per page
2. Scraper: Max 100 pages
3. Watcher: Fixed check intervals

---

 **Pydantic Improvements**
The project uses **Pydantic** for data modeling and validation, replacing the previous `dataclass` implementation. Below are the key improvements achieved by using Pydantic:

 **Comparison Table: `dataclass` vs Pydantic**

| Feature                  | `dataclass`                          | Pydantic (`BaseModel`)               |
|--------------------------|--------------------------------------|--------------------------------------|
| **Data Validation**       | No built-in validation               | Automatic validation of fields       |
| **Serialization**         | Manual serialization required        | Built-in `.model_dump()` and `.model_dump_json()` |
| **Type Enforcement**      | Type hints only (no runtime checks)  | Runtime type checking and coercion   |
| **Error Handling**        | Manual error handling                | Automatic error messages for invalid data |
| **Default Values**        | Supported                           | Supported with additional features   |
| **Complex Data Types**    | Limited support                     | Advanced support (e.g., nested models, custom validators) |

 **Benefits of Pydantic**
1. **Data Validation**:
   - Ensures that all fields in the `Question` object adhere to their defined types. For example, if `id` is not an integer, Pydantic will raise a `ValidationError` immediately, making debugging easier.

2. **Serialization**:
   - Simplifies converting `Question` objects to dictionaries or JSON using `.model_dump()` or `.model_dump_json()`. This is useful for storing or transmitting data.

3. **Error Handling**:
   - Provides detailed error messages when validation fails, making it easier to identify and fix issues.

4. **Type Safety**:
   - Enforces type hints at runtime, reducing the risk of bugs caused by incorrect data types.

5. **Flexibility**:
   - Supports advanced features like nested models, custom validators, and default values, which are useful as the application grows.

 **Example of Pydantic Validation**
If invalid data is provided, Pydantic raises a `ValidationError` with detailed error messages:

```python
from models import Question

 This will raise a ValidationError because 'id' is not an integer
try:
    invalid_question = Question(
        id="not_an_integer",
        title="Test Question",
        link="https://stackoverflow.com",
        excerpt="This is a test question",
        tags=["python", "pydantic"],
        timestamp="2023-10-01T12:00:00Z"
    )
except Exception as e:
    print(f"Validation Error: {e}")
```

Output:
```
Validation Error: 1 validation error for Question
id
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not_an_integer', input_type=str]
```

---

 **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---