# Autonomous Metadata-Driven RAG Orchestrator

## 🏗️ System Architecture
```mermaid
graph TD
    User((User)) --> API[FastAPI Gateway]
    API --> Agent[LangGraph Orchestrator]
    
    subgraph "Knowledge Layer"
        Agent --> Embed[Embedding Service: OpenAI]
        Embed --> VDB[(PostgreSQL + pgvector)]
    end

    subgraph "Database Engineering Layer"
        Agent --> SQLGen[LLM SQL Generator]
        SQLGen --> Metadata[(Metadata Registry)]
        Metadata --> DB[(Source Relational DB)]
    end
