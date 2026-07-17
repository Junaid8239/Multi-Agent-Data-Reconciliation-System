# Multi-Agent Data Reconciliation & Formatting Engine

An autonomous multi-agent system that extracts, validates, and reformats messy customer records against a live SQL Server database — built with CrewAI, powered by Groq, wrapped in FastAPI, and deployed as a Docker container.

**Live API:** https://multi-agent-data-reconciliation-system.onrender.com
*(hosted on Render's free tier — the first request after a period of inactivity may take 30-60s to wake up)*

---

## What it does

Given messy, inconsistently formatted input like:

```
"jon smith , jsmith@gmail.com, 555-123-4567"
```

the system autonomously:
1. **Extracts** structured fields (name, email, phone) from the raw text
2. **Validates** those fields against a real customer database, using fuzzy matching to handle typos, casing, and formatting differences
3. **Formats** the result into a clean, standardized JSON record

...with zero manual data entry or hardcoded parsing rules — three specialized AI agents handle each step and hand off context to one another in sequence.

## Architecture

```
                ┌─────────────────────────────────────────┐
                │              FastAPI Service              │
                │   POST /reconcile { raw_records: [...] }  │
                └───────────────────┬─────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │      CrewAI Crew       │
                        │  (sequential process)  │
                        └───────────┬───────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐          ┌────────────────────┐      ┌────────────────┐
│ Data Extractor │  --->   │ Database Validator  │ ---> │   Formatter    │
│ (Agent 1)      │         │ (Agent 2)           │      │ (Agent 3)      │
│ parses/cleans  │         │ fuzzy-matches vs    │      │ produces final │
│ raw input      │         │ SQL Server records  │      │ structured JSON│
└───────────────┘          └────────────────────┘      └────────────────┘
                                    │
                                    ▼
                          SQL Server (Azure SQL Database)
                                    │
                                    ▼
                          Groq API (LLM reasoning — Llama 3.3 70B)
```

Each agent has a single responsibility and its own custom Python tool — this is what makes it a genuine multi-agent workflow rather than one large prompt.

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | [CrewAI](https://github.com/crewAIInc/crewAI) |
| LLM inference | [Groq](https://groq.com/) (Llama 3.3 70B Versatile) |
| API framework | FastAPI |
| Database | Microsoft SQL Server (Azure SQL Database) |
| Fuzzy matching | [thefuzz](https://github.com/seatgeek/thefuzz) |
| Containerization | Docker |
| Hosting | Render (API) + Azure SQL Database (data) |

## Project Structure

```
data-reconciliation-engine/
├── app/
│   ├── main.py                  # FastAPI entrypoint
│   ├── crew.py                  # CrewAI crew + task definitions
│   ├── schemas.py                # Pydantic request/response models
│   ├── config.py                 # Environment variable loading
│   ├── agents/
│   │   └── agent_configs.py     # Agent role/goal/backstory definitions
│   ├── tools/
│   │   ├── extraction_tool.py    # Parses raw text into structured fields
│   │   ├── db_validator_tool.py  # Fuzzy-matches against SQL Server
│   │   └── formatter_tool.py     # Produces the final standardized record
│   └── db/
│       └── session.py            # SQLAlchemy engine/session setup
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml            # Local dev: spins up SQL Server + API together
└── setup_reconciliation_db_azure.sql
```

## Running Locally

### Prerequisites
- Python 3.12
- Docker Desktop
- A [Groq API key](https://console.groq.com/keys)
- Access to a SQL Server instance (local via Docker Compose, or Azure SQL)

### Setup

```bash
git clone https://github.com/Junaid8239/Multi-Agent-Data-Reconciliation-System.git
cd Multi-Agent-Data-Reconciliation-System

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # fill in your Groq key + database credentials
```

### Run with Docker Compose (spins up SQL Server + the API together)

```bash
docker compose up --build
```

### Or run the API locally against any SQL Server instance

```bash
uvicorn app.main:app --reload --port 8000
```

### Test it

```bash
curl -X POST http://localhost:8000/reconcile \
  -H "Content-Type: application/json" \
  -d '{"raw_records": ["jon smith , jsmith@gmail.com, 555-123-4567"]}'
```

## API Reference

### `GET /health`
Returns `{"status": "ok"}` — used for uptime checks.

### `POST /reconcile`

**Request:**
```json
{
  "raw_records": [
    "jon smith , jsmith@gmail.com, 555-123-4567",
    "Maria Garcia - mgarcia@yahoo.com - 555-987-6543"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "input_name": "jon smith",
      "input_email": "jsmith@gmail.com",
      "input_phone": "555-123-4567",
      "matched_in_db": true,
      "customer_id": 1,
      "canonical_name": "Jon Smith",
      "canonical_email": "jsmith@gmail.com",
      "canonical_phone": "555-123-4567",
      "canonical_address": "12 Elm St",
      "match_confidence": 100
    }
  ]
}
```

Interactive Swagger docs are available at `/docs` on any running instance (e.g. https://multi-agent-data-reconciliation-system.onrender.com/docs).

## Deployment

- **API** is containerized with Docker and deployed on **Render**, which builds directly from this repo's `Dockerfile` on every push to `main`.
- **Database** runs on **Azure SQL Database** (serverless, free tier).
- Secrets (Groq API key, database credentials) are configured as environment variables in Render's dashboard — never committed to source control.

## Notes & Known Limitations

- This is a portfolio/demo project — the Azure SQL firewall currently allows broad inbound access to accommodate Render's free tier (which doesn't expose a fixed outbound IP range). A production deployment would use private networking or a static-IP tier instead.
- Render's free tier spins the service down after inactivity; the first request after idling will be slower while it wakes up.
- Fuzzy matching uses a similarity threshold of 75% (`thefuzz`); this is tunable in `app/tools/db_validator_tool.py`.

