# Magicpin Vera AI Challenge - Backend

This is a submission-ready backend service built with FastAPI that implements Vera-like AI messaging.

## Requirements

- Python 3.8+
- Requirements specified in `requirements.txt`

## Installation

1. Clone or navigate to the project directory.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application Locally

Run the following command to start the development server:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.
You can access the interactive Swagger API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

1. `POST /v1/context`: Stores context payload containing `category`, `merchant`, `trigger`, and an optional `customer`. Returns a `context_id`.
2. `POST /v1/tick`: Accepts a JSON payload with `context_id` and runs the core messaging logic to compose and return the message.
3. `POST /v1/reply`: Accepts merchant replies (`merchant_id` and `reply_text`) and returns a contextual response based on simple intent matching. It also detects auto-replies.
4. `GET /v1/healthz`: Returns the system health status (`{"status": "ok"}`).
5. `GET /v1/metadata`: Returns the bot metadata.

## Core Logic (`bot.py`)

The `compose()` function handles context evaluation and builds messages deterministically based on:
- `perf_dip`: Mentions performance drop + suggests profile optimization.
- `research_digest`: Shares industry insight on photos.
- `festival_upcoming`: Suggests an offer from the `offer_catalog`.
- `recall_due`: Creates a customer reminder.
- Calculates `send_as` correctly based on whether a `customer` exists in the context.

The `handle_reply()` function matches basic intent (YES / NO) and detects repetitive auto-replies for graceful message exits.
