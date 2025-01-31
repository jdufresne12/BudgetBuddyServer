## Backend Initialization & Structure
---
### Project Structure
```
.
├── api/
│   ├── dependencies/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── .gitignore
├── Dockerfile
└── README.md
```

**Models:** Database table definitions that map your python classes to database tables, handling data relationships and constraints

**Routers:** Define your API endpoints and HTTP methods (GET, POST, etc.) directing incoming requests to the appropriate handler functions

**Schemas:** Define the structure and validation rules for the request/response data, ensuring data consistency and providing automatic validation

**Services:** Contain core business logic and complex operations, acting as an intermediary layer between routes and modules to keep code modular

### Typical API Flow
1. Router receives HTTP request
2. Schema validates incoming request data
3. Router calls appropriate Service
4. Service implements business logic, interacting with Models for database operations
5. Service returns data back through Router
6. Schema validates outgoing response data
7. Router sends HTTP Response

### Creating a Virtual Environment (venv)
```python
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

**venv**'s creates an isolated python environment with its own dependencies, preventing conflicts between different project's package versions and keeping your global python Installation clean

### Docker Environment
```Dockerfile
# Dockerfile

# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
```

#### Building and Running
```bash
# Build Docker image
docker build -t my-python-backend .

# Run Docker container
docker run -p 5000:5000 my-python-backend
```
#### Helpful Commands
```bash
# Shows all docker containers 
docker ps

# Test the API endpoint
curl http://localhost:8000/

# Clearing Resources (Containers/Images/Volumes)
docker compose down 
docker system prune -a --volumes
docker volume ls

# Connect to the database
docker exec -it <postgres_container_id> psql -U user -d budgetdb
```

