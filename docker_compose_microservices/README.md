# Multi-Container Infrastructure using Docker Compose

## Requirements
- Docker Desktop installed and running
- Windows PowerShell or Command Prompt

## Run
Open a terminal in this folder (the folder containing docker-compose.yml) and run:

```bash
docker compose up -d --build
```

Check containers:

```bash
docker ps
```

Test in your browser:

http://localhost:8080/api/data

Expected JSON (the id may differ):

```json
{
  "data": [
    {
      "id": 1,
      "message": "Hello from the Dockerized microservice!"
    }
  ],
  "message": "Connected to PostgreSQL successfully",
  "status": "success"
}
```

## Optional POST test using Postman
- Method: POST
- URL: http://localhost:8080/api/data
- Body > raw > JSON:

```json
{
  "message": "Experiment tested successfully"
}
```

Refresh the GET URL to see the added record.

## Useful commands

```bash
docker compose ps
docker compose logs app-service
docker compose logs app-db
docker compose down
```

To remove containers and database storage:

```bash
docker compose down -v
```

Warning: `down -v` deletes the stored database data.

## How it works
Both services use the shared Docker network `app-network`.
The Flask app connects to PostgreSQL using hostname `app-db` and port `5432`.
Docker Compose resolves service names automatically on this network.
Host port 8080 maps to port 8080 inside the app container.
