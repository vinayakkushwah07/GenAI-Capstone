
# GenAI Capstone Project

A FastAPI-based generative AI application with authentication, RAG (Retrieval-Augmented Generation) pipeline, and graph-based query routing.

## Project Structure

```
genAi/
├── api/v1/                    # API endpoints
│   ├── auth_endpoint.py       # Authentication routes
│   ├── graph_endpoint.py      # Graph processing routes
│   └── rag_upload_endpoint.py # Document upload & RAG routes
├── core/                      # Core utilities
│   ├── auth.py               # Authentication logic
│   ├── password.py           # Password handling
│   └── settings.py           # Configuration
├── data_pipeline/            # Data processing
│   ├── chunker.py            # Document chunking
│   ├── build_embedding.py    # Embedding generation
│   ├── add_to_vdb.py         # Vector DB integration
│   ├── file_pre_proc.py       # File processing
│   └── [other processors]    # Additional pipeline modules
├── database/                 # Database layer
│   ├── dbconn.py            # Database connection
│   └── db_dep.py            # Database dependencies
├── gen_ai/                   # AI model core
│   ├── core_model.py         # Base model
│   ├── graph.py              # Graph implementation
│   └── nodes.py              # Graph nodes
├── model/                    # Data models
│   ├── my_users.py           # User & Chat models
│   ├── chat_model.py         # Chat message models
│   ├── context.py            # Context model
│   └── token_model.py        # Token models
├── schemas/                  # Pydantic schemas
│   ├── main_user_schema.py   # User schemas
│   ├── access_role.py        # Role schemas
│   └── metadata_schemas.py   # Metadata schemas
├── service/                  # Business logic
│   ├── user_crud.py          # User operations
│   ├── get_current_user.py   # User retrieval
│   └── memory_data.py        # Memory management
├── main.py                   # Application entry point
└── readme.md                 # This file
```

## Features

- **Authentication**: User login and token management
- **RAG Pipeline**: Document ingestion, chunking, embedding, vector storage and role-based access control
- **Graph-Based Routing**: Intelligent query classification and routing
- **Chat Interface**: Conversation management with context awareness
- **User Management**: CRUD operations and role-based access control

## Installation

```bash
    pip install -r req.txt

    cd chroma
```

## Running the Application

```bash
python main.py
```

The API will start at `http://0.0.0.0:8000`

## API Endpoints

- `POST /auth/*` - Authentication endpoints
- `POST /upload/*` - RAG document upload
- `POST /graph/*` - Graph query endpoints

## Graph Visualization
![image description](./Graph.png)