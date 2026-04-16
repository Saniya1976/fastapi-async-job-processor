# ⚡ FastAPI Async Job Processor

A clean, production-grade template demonstrating how to handle **long-running background tasks** without making your users wait. Built with FastAPI and SQLAlchemy using **Clean Architecture** principles.

---

### 🏛 The Restaurant Analogy (How it Works)
Imagine you are at a busy restaurant:
1. **The Order (POST /jobs)**: You place your order. The waiter (API) immediately gives you a **Token (Job ID)** and says, *"I've put your order in the queue."*
2. **The Kitchen (Background Task)**: While you sit comfortably at your table (client), the chef (Background Worker) is busy cooking your meal in the background.
3. **Checking Status (GET /jobs/{id})**: You can look at the "Order Ready" screen (Poll the API) to see if your token is still *Pending*, *In Progress*, or *Ready (Completed)*.

**This is Asynchronous Processing.** The waiter isn't standing at your table for 20 minutes; he is free to take other orders while your meal is prepared.

---

## 🌟 Features
- **Non-Blocking Logic**: User receives immediate feedback while heavy processing happens in the background.
- **Clean Architecture**: Strictly separated layers (**API → Services → Models**) for maximum maintainability.
- **Unified API Response**: Every response follows the `{ success, data, message }` standard.
- **Resilient Worker**: If a background task crashes, it gracefully updates the DB to a `failed` state with error details.
- **UUID Security**: Uses UUID4 for job tracking to prevent ID guessing.
- **Comprehensive Logging**: Detailed terminal logs for every stage of the job lifecycle.

## 🛠 Tech Stack
- **FastAPI**: Modern, high-performance web framework.
- **SQLAlchemy 2.0**: The industry-standard Python ORM.
- **Pydantic V2**: Powerful data validation and settings management.
- **SQLite**: Lightweight, zero-config relational database.
- **AsyncIO**: Python's native concurrency for non-blocking I/O.

## 📂 Project Structure
```text
app/
├── api/          # HTTP Controllers (Request/Response handling)
├── services/     # Business Logic & Async Background Workers
├── models/       # Database Schema (SQLAlchemy Models)
├── schemas/      # Data Validation (Pydantic Models)
└── db/           # Database Engine & Session config
```

## 🚥 Key Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/jobs/` | Queue a new job (Returns Job ID immediately) |
| `GET` | `/jobs/` | List all jobs (Sorted Latest First) |
| `GET` | `/jobs/{id}`| Check real-time status/result of a job |

## 📦 Getting Started

1. **Install Dependencies**:
```bash
<<<<<<< HEAD
git clone https://github.com/Saniya1976/fastapi-async-job-processor
cd fastapi-async-job-processor
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
=======
>>>>>>> 6369577 (Developed asynchronous job processing backend using FastAPI with background tasks, status tracking, and clean architecture)
pip install -r requirements.txt
```

2. **Run the Server**:
```bash
uvicorn app.main:app --reload
```

3. **Check it out**: 
Open `http://localhost:8000/docs` to test the API interactively.

---

## � Example: Clean JSON Responses
<img width="800" height="651" alt="image" src="https://github.com/user-attachments/assets/aa47b2ad-7ddf-439a-b927-c50f876f17b3" />
<img width="800" height="601" alt="image" src="https://github.com/user-attachments/assets/f5eba6e0-1d58-4c5d-988a-0e043016d46f" />

**Successful Query**:
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "result": "Task completed successfully after 7.42s"
  },
  "message": "Job details retrieved successfully"
}
```
<img width="800" height="612" alt="image" src="https://github.com/user-attachments/assets/66c5936d-6513-4186-98c0-08448bb1e42d" />

**Job Not Found (Error)**:
```json
{
  "success": false,
  "data": null,
  "message": "Job with ID ... not found in the system"
}
```
<img width="800" height="558" alt="image" src="https://github.com/user-attachments/assets/f8fe7ae5-8e36-405a-a88e-328b4e1d60ba" />

---
*Developed with a focus on **Clarity**, **Maintainability**, and **Performance**.*
