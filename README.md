# 🚚 Customer Support Agent

A conversational AI agent built with **Google ADK 2.0** that acts as a customer support representative for a shipping company. It uses a **graph workflow** to intelligently classify and route user queries.

## How It Works

```
User Query
    │
    ▼
┌─────────────────┐
│  Classifier     │  LlmAgent — determines if query is shipping-related
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌────────┐  ┌──────────┐
│  FAQ   │  │ Decline  │
│ Agent  │  │  Node    │
└────────┘  └──────────┘
 shipping     unrelated
```

1. **Classifier** — An `LlmAgent` reads the user query and outputs a category: `shipping` or `unrelated`.
2. **Router** — A function node reads the category from state and emits a `route` to branch the workflow.
3. **Shipping FAQ Agent** — An `LlmAgent` answers questions about rates, tracking, delivery times, and returns.
4. **Decline Node** — Politely informs the user it can only answer shipping-related questions.

## Shipping FAQ Coverage

| Topic | Details |
|---|---|
| **Rates** | Standard $5.99 · Express $12.99 · Free standard on orders over $50 |
| **Tracking** | Enter tracking number on the website's tracking page |
| **Delivery** | Standard 3–5 business days · Express 1–2 business days |
| **Returns** | Free returns within 30 days of delivery in original condition |

## Project Structure

```
Agent-project/
├── customer-support-agent/
│   ├── agent.py        # Workflow definition (main entry point)
│   ├── __init__.py
│   └── .env            # Your API key (not committed)
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Google ADK 2.0 (`pip install google-adk`)
- A [Google AI Studio API key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repo
git clone https://github.com/ianosebe/Customer-Suport-Agent.git
cd Customer-Suport-Agent

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install google-adk
```

### Configuration

Create a `.env` file inside the `customer-support-agent/` folder:

```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_ENTERPRISE=0
```

### Running the Agent

**Interactive CLI:**
```bash
adk run customer-support-agent
```

**Web Playground UI:**
```bash
adk web
# Open http://127.0.0.1:8000 in your browser
```

## Example Interactions

| User Query | Response |
|---|---|
| *"What is the shipping rate?"* | Answers from the FAQ (Standard $5.99, Express $12.99...) |
| *"How do I track my order?"* | Explains how to use the tracking page |
| *"What is the capital of France?"* | Politely declines — outside shipping scope |

## Built With

- [Google ADK 2.0](https://google.github.io/adk-docs/) — Agent Development Kit
- [Gemini](https://ai.google.dev/) — LLM for classification and FAQ answering
- [Pydantic](https://docs.pydantic.dev/) — Structured output schema
