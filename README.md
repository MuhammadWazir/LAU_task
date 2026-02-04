# Python Implementation

## Setup
1. Ensure you have Docker and Docker Compose installed.
2. Clone the repository and navigate to the `python_implementation` directory.
3. (Optional) If running locally without Docker:
    - Install Python 3.10+.
    - Install dependencies: `pip install -e .` (or use `uv sync`).
    - Ensure a PostgreSQL instance and Redis instance are running.
    - Set up the environment variables in a `.env` file.

## Run Instructions
Run the entire stack (API, PostgreSQL, Redis) using Docker Compose:
```powershell
docker-compose up --build
```
The API will be available at `http://localhost:8000`.
FastAPI Interactive documentation (Swagger) can be accessed at `http://localhost:8000/docs`.

## Test Commands
To run tests using the local environment:
```powershell
pytest
```
To run tests via the provided helper script:
```powershell
python tests/run_tests.py
```

## Sample CURL Requests

### Create a Task
```bash
curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Complete Python Implementation"}'
```

### List Tasks
```bash
curl "http://localhost:8000/tasks?status=OPEN&limit=10&offset=0"
```

### Get Task by ID
```bash
curl http://localhost:8000/tasks/<task_id>
```

### Complete a Task
```bash
curl -X PATCH http://localhost:8000/tasks/<task_id>/complete
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/tasks/<task_id>
```


# Java Implementation

## Setup
1. Ensure you have Docker and Docker Compose installed.
2. Clone the repository and navigate to the `java_implementation` directory.
3. (Optional) If running locally without Docker:
    - Install Java 17.
    - Install Maven.
    - Ensure a PostgreSQL instance and Redis instance are running.

## Run Instructions
Run the entire stack (API, PostgreSQL, Redis) using Docker Compose:
```powershell
docker-compose up --build
```
The API will be available at `http://localhost:8080`.
Swagger UI documentation can be accessed at `http://localhost:8080/swagger-ui/index.html`.

## Test Commands
To run tests using Docker (sharing the host Docker socket for Testcontainers):
```powershell
docker run --rm `
  -e TESTCONTAINERS_RYUK_DISABLED=true `
  -v ${PWD}:/app `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -w /app `
  maven:3.8.4-openjdk-17-slim `
  mvn test
```
To run tests locally using Maven:
```powershell
mvn test
```

## Sample CURL Requests

### Create a Task
```bash
curl -X POST http://localhost:8080/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Complete Java Implementation"}'
```

### List Tasks
```bash
curl "http://localhost:8080/tasks?status=OPEN&limit=10&offset=0"
```

### Get Task by ID
```bash
curl http://localhost:8080/tasks/<task_id>
```

### Complete a Task
```bash
curl -X PATCH http://localhost:8080/tasks/<task_id>/complete
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8080/tasks/<task_id>
```
