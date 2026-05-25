# AGENTS.md

## Project Overview

This project is an AI-powered executive assistant automation platform.

Main goals:

- Read and classify emails
- Generate AI draft replies
- Create meeting summaries
- Generate pre-meeting briefs
- Send Telegram notifications
- Track follow-ups and reminders
- Store chat history when conversational workflows need memory
- Store vector documents in PostgreSQL with pgvector when retrieval is needed

This is a backend-first architecture using FastAPI, LangGraph, LangChain tools, and MCP.

## Architecture

Use capability-oriented modules instead of clean architecture layers:

- `agents`: AI-facing behavior and prompting decisions.
- `workflows`: LangGraph orchestration.
- `tools`: LangChain-compatible tool factories and registry.
- `integrations`: Gmail, Calendar, Telegram, and model-provider adapters.
- `operations`: use-case coordination used by API, MCP, workers, and tools.
- `api`: FastAPI route classes and dependency wiring.
- `mcp`: Model Context Protocol server and tools.
- `storage`: repository contracts and concrete persistence implementations.
- `models`, `schemas`, `config`, `workers`, and `prompts`: shared support code.

Keep dependency flow pragmatic: routes, MCP tools, workers, and LangChain tools call
operations; operations coordinate agents, workflows, integrations, and storage.

## Current Functional Status

Working locally:

- Health check endpoint
- Deterministic email classification
- Deterministic draft reply generation
- Meeting transcript summary drafts
- Pre-meeting brief drafts
- Follow-up creation and listing with in-memory storage
- Optional PostgreSQL follow-up persistence
- PostgreSQL chat history repository and API routes
- PostgreSQL pgvector document repository and API routes
- Telegram notification delivery when bot credentials are configured
- LangChain tool registry for email, meeting, and notification actions
- LangGraph email classification workflow builder

Still provider-dependent:

- Google Calendar API event reads
- Embedding generation before storing/searching pgvector documents

## Tech Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn

### AI / Agents

- LangGraph
- LangChain
- Gemini or Claude

### Database

- PostgreSQL
- pgvector
- In-memory local fallback for follow-ups

### Scheduling

- APScheduler

### External Services

- Gmail API
- Google Calendar API
- Telegram Bot API

## Configuration

Copy `.env.example` to `.env` and edit values as needed.

Important settings:

- `FOLLOWUP_REPOSITORY=memory` uses local in-memory follow-up storage.
- `FOLLOWUP_REPOSITORY=postgres` uses PostgreSQL and auto-creates the `followups` table.
- `DATABASE_URL` is required for PostgreSQL-backed follow-ups, chat history, and vectors.
- `VECTOR_DIMENSION` controls the pgvector column dimension.
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_DEFAULT_CHAT_ID` are required for real Telegram delivery.
- `AI_PROVIDER=openai` enables OpenAI-backed AI behavior.
- `OPENAI_API_KEY` is required when `AI_PROVIDER=openai`.

## Run Locally

```powershell
pip install -r requirements-dev.txt
uvicorn src.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Development Rules

### Structure Rules

- Keep AI behavior in `src/agents`.
- Keep use-case orchestration in `src/operations`.
- Keep SQL, memory stores, and other data-source details in `src/storage`.
- Keep external provider implementations in `src/integrations`.
- Keep business logic out of API routes.
- API routes should delegate to operations.
- Use dependency injection through `src/api/dependencies.py`.
- Prefer composition over inheritance.
- Keep code class-based for orchestration components.
- Use Google-style docstrings for public classes and methods.

### Repository Rules

- A repository is required only when code talks to a data source.
- Repository contracts and implementations belong in `src/storage`.
- PostgreSQL repositories should initialize only the tables/extensions they own.
- Use pgvector through PostgreSQL for vector storage and similarity search.

### Service Rules

- Services are external provider implementations.
- Service contracts and implementations belong in `src/integrations`.
- Services may perform HTTP/provider operations.
- Use cases should depend on service contracts, not concrete providers.

### File Size and Function Rules

- Keep files focused on one responsibility.
- Split large methods into private helper methods when logic grows.
- Avoid mixing SQL, HTTP, AI prompting, and API routing in one class.
- Prefer small route classes, use cases, repositories, and provider clients.

### Agent, Graph, and Prompt Rules

- Agents own AI-facing behavior.
- LangChain tools live in `src/tools`.
- LangGraph builders live in `src/workflows`.
- Prompt content lives in Markdown files under `src/prompts`.

## Folder Structure

```text
src/
|-- agents/
|-- api/
|   `-- routes/
|-- config/
|-- integrations/
|   |-- ai/
|   |-- calendar/
|   |-- gmail/
|   `-- telegram/
|-- mcp/
|-- models/
|-- operations/
|-- prompts/
|-- schemas/
|-- storage/
|   `-- database/
|-- tools/
|-- workers/
|-- workflows/
`-- main.py
```
