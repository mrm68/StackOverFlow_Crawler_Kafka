**README.md**  

```markdown
# StackOverflow Python Question Monitor  
*Dockerized crawler tracking new Python questions on StackOverFlow. Features HTML scraping, state persistence, and code visualization. Includes logging decorators for method tracing.*  

---

## 🛠️ **Run with Docker**  
**1. Run Crawler**:  
```bash  
docker build -f Dockerfile.crawler -t crawler .  
docker run --rm crawler  # Saves last_seen_id_python.txt  
```  

**2. Generate Code Diagrams**:  
```bash  
docker build -f Dockerfile.diagrams -t diagrams .  
docker run -v $(pwd)/diagrams:/app/diagrams --rm diagrams  
```  

---

## 📂 **Code Structure**  
```  
.  
├── Dockerfile.crawler        # Builds crawler image  
├── Dockerfile.diagrams       # Generates code2flow diagrams  
├── StackOverFlow_Crawler_Kafka/  
│   ├── Crawler/  
│   │   ├── fetcher.py        # Fetches HTML with retries (FetcherStrategy)  
│   │   ├── parser.py         # Extracts Q&A via BeautifulSoup (QuestionParserTemplateMethod)  
│   │   ├── watcher.py        # Polls for new questions (QuestionWatcher)  
│   │   ├── notification_handler.py  # Handles 15+ event types (Notifier + NotificationType enum)  
│   │   └── tracedecorator.py # Logs method entries/exits to usage.log  
│   ├── main.py               # CLI entry point with dependency setup  
│   └── models.py             # Pydantic models (Question, Constants, ParsConstants)  
```  

---

## 🧩 **Core Components**  
| File/Class | Key Features |  
|------------|--------------|  
| **fetcher.py** | Retry logic (3 attempts), User-Agent rotation, URL builder |  
| **parser.py** | CSS selectors for StackOverFlow DOM, Question data extraction |  
| **watcher.py** | Persistent state (last_seen_id), Interval polling (60s default) |  
| **notification_handler.py** | 15+ event types (FETCH_FAILED, NEW_QUESTIONS, etc.) |  
| **tracedecorator.py** | Logs method calls/errors with timestamps to usage.log |  

---

## 🔍 **Key Data Structures**  
1. **Question** (models.py):  
   - ID, title, link, tags, votes, answers, views  
   - Pydantic model for validation  
2. **Constants**:  
   - Configurable parameters (user agent, scrape interval, max questions)  

---
