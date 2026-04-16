# FastAPI Async Job Processor

A professional, production-ready FastAPI backend implementing a **Clean Architecture** pattern for asynchronous job processing. This project demonstrates how to handle long-running tasks in the background while keeping the API responsive and maintaining a structured data layer.

## 🚀 Features

- **Asynchronous Processing**: Uses FastAPI's `BackgroundTasks` for non-blocking job execution.
- **Clean Architecture**: Decoupled layers for API, Services, Models, and Schemas.
- **Unified Response Format**: All API responses follow a consistent `{ success, data, message }` structure.
- **Robust Error Handling**: Global exception handlers for 404s, 500s, and validation errors.
- **UUID Identifiers**: Uses UUID4 for job identification to ensure security and uniqueness.
- **Randomized Simulation**: Background tasks include random delays (5-10s) and success/failure outcomes to simulate real-world conditions.
- **Automated Logging**: Comprehensive tracking of job lifecycles (creation, start, completion, failure).
- **SQLite Database**: Lightweight storage using SQLAlchemy 2.0.

## 🛠 Tech Stack

- **Core**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (SQLite)
- **Validation**: [Pydantic V2](https://docs.pydantic.dev/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Async**: Python `asyncio`

## 📂 Project Structure

```text
app/
├── api/          # API route handlers & controllers
├── db/           # Database configuration & session management
├── models/       # SQLAlchemy database models
├── schemas/      # Pydantic schemas (Request/Response/Generic)
├── services/     # Business logic & Background tasks
└── main.py       # Application entry point & configuration
```

## 🚥 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/jobs/` | Create a new job and start background processing |
| `GET` | `/jobs/` | List all jobs sorted by creation date (latest first) |
| `GET` | `/jobs/{id}`| Get the current status and result of a specific job |
| `PATCH`| `/jobs/{id}`| Manually update job fields (internal/admin) |
| `DELETE`| `/jobs/{id}`| Remove a job record from the database |

## 📦 How to Run Locally

### 1. Clone the repository
```bash
git clone <repository-url>
cd fastapi-async-job-processor
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive documentation at `http://localhost:8000/docs`.

## 📝 Example API Responses

### Success Response (Job Created)
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "result": null,
    "created_at": "2024-03-20T12:00:00Z",
    "updated_at": "2024-03-20T12:00:00Z"
  },
  "message": "Job created and processing started"
}
```

### Error Response (Job Not Found)
```json
{
  "success": false,
  "data": null,
  "message": "Job with ID 550e8400... not found"
}
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
