# Restaurant Chatbot Demo

A restaurant customer-support chatbot with built-in lead capture. It answers questions about the menu, ingredients, timings, and location using Google Gemini grounded in the restaurant's menu data. It also has a small CRM layer for saving leads and orders. FastAPI provides the back end and Streamlit the demo UI.

## Features

- **Menu-aware assistant** — Gemini answers from a menu context, with a defined persona, off-topic handling, and multilingual replies.
- **Menu API** — list, search, and look up menu items.
- **Lead capture** — the chat UI collects a customer's name and phone number and saves them as a lead through the API.
- **Orders and leads endpoints** — create and list leads and orders.
- **Layered structure** — separate API, services, models, and config layers, with settings loaded from the environment.

## Tech Stack

Python · FastAPI · Pydantic · Google Gemini (`google-generativeai`) · Streamlit

## Project Structure

```
├── main.py              # FastAPI app and router wiring
├── demo_ui.py           # Streamlit demo UI
└── app/
    ├── api/             # routes (CRM), menu, gemini chat
    ├── services/        # gemini_service, menu_service, lead_service
    ├── models/          # Lead and Order models
    └── core/config.py   # Settings loaded from .env
```

## Getting Started

```bash
git clone https://github.com/huzaifa1134/Restaurant_Chatbot_Demo.git
cd Restaurant_Chatbot_Demo

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
APP_NAME=Restaurant Chatbot Demo
DEBUG=true
GOOGLE_API_KEY=your_google_api_key
```

```bash
# Back end
uvicorn main:app --reload --port 8000

# Front end (set API_BASE_URL in demo_ui.py to http://localhost:8000 for local use)
streamlit run demo_ui.py
```

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/gemini/chat` | Ask the assistant a question |
| GET | `/menu/` | List menu items |
| GET | `/menu/search` | Search menu items |
| GET | `/menu/{item_id}` | Get one menu item |
| POST / GET | `/crm/leads` | Create or list leads |
| POST / GET | `/crm/orders` | Create or list orders |

Interactive docs are at `/docs` while the server is running.

## Notes

Leads and orders are stored in memory, so they reset when the server restarts. Swap `lead_service.py` for a database to persist them.

## Author

**Huzaifa Jawed** — [GitHub](https://github.com/huzaifa1134) · [LinkedIn](https://www.linkedin.com/in/huzaifa-jawed-030ab7275/)
