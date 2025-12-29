# Project Overview

This project is a simple ETL (Extract, Transform, Load) pipeline orchestrated with Docker Compose. It consists of two main services:

*   **`etl-job`**: A Python application that connects to a PostgreSQL database, extracts data from a `pracownicy` table, and prints a report to the console.
*   **`warehouse`**: A PostgreSQL database instance, pre-populated with sample data.

The project demonstrates a basic data processing workflow and the use of Docker for creating a reproducible development environment.

## Workflow Diagram

```mermaid
sequenceDiagram
    participant User
    participant DockerCompose
    participant ETLJob as etl-job
    participant Warehouse as warehouse (Postgres)

    User->>DockerCompose: Executes `docker-compose up --build`
    
    Note over DockerCompose: Reads docker-compose.yaml and respects `depends_on`

    DockerCompose->>Warehouse: Start container from `postgres:15-alpine` image
    activate Warehouse
    Warehouse-->>Warehouse: PostgreSQL server starts
    Warehouse-->>Warehouse: Executes `init.sql` (creates and populates table)
    Note right of Warehouse: Database is now ready to accept connections
    deactivate Warehouse
    
    DockerCompose->>ETLJob: Build image from `./backend/Dockerfile`
    activate ETLJob
    DockerCompose->>ETLJob: Start container and run `python main.py`

    Note over ETLJob: Script starts...
    ETLJob->>Warehouse: Attempt to connect to database
    
    loop Healthcheck/Retry Loop
        Warehouse-->>ETLJob: Connection fails (database is still starting up)
        ETLJob-->>ETLJob: Wait 5 seconds and retry
        ETLJob->>Warehouse: Attempt to connect to database
    end

    Warehouse-->>ETLJob: Connection successful!
    ETLJob->>Warehouse: Execute `SELECT * FROM pracownicy`
    activate Warehouse
    Warehouse-->>ETLJob: Return rows
    deactivate Warehouse
    
    ETLJob-->>ETLJob: Process and print data to stdout
    deactivate ETLJob

    Note over DockerCompose: Both containers are now running
```
