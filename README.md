# API

## Project Structure

```
./
├── src/
│   ├── adapters/      # Adapters (Database (driven) and FastAPI (driving))
│   ├── core/          # Core application logic
│   ├── domain/        # Entities and interfaces (ports)
│   ├── infrastructure/# Database repositories (adapters)
│   └── main.py        # FastAPI entrypoint
├── tests/             # Unit and integration tests
├── requirements.txt   # Python dependencies
└── README.md
```

## Key Concepts

- **Hexagonal Architecture**: Separates business logic from external concerns (like APIs and databases) using ports (interfaces) and adapters (implementations).
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+.

## Getting Started

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the API**:
    ```bash
    uvicorn app.main:app --reload
    ```

3. **Access documentation**:  
    Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

## Folder Descriptions

- `api/`: Defines API endpoints and request/response models.
- `domain/`: Contains business entities and interfaces (ports).
- `infrastructure/`: Implements adapters for database and external services.
- `core/`: Application services and use cases.

# How to implement coding in this solution
Create an Interface with abstract methods, create the repository for database with the collection and the Entity to be created and for last, create the router for exposing api

# Docker exec 
```bash
docker build -f src/infrastructure/docker/Dockerfile -t IMAGE .
docker run -p 8000:8000 --name NAME IMAGE

```

# MINIKUBE Runserver
```
minikube addons enable metrics-server
minikube stop
minikube delete
minikube start --addons=metrics-server --memory=4096 --cpus=2          
minikube service IMAGE --url

```