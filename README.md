# 🎓 Student Management System

A beginner-friendly full-stack web application built with **FastAPI** (Backend), **SQLite + SQLAlchemy** (Database), and **Streamlit** (Frontend).

---

## 1. Project Overview

The **Student Management System** allows users to perform complete **CRUD** (Create, Read, Update, Delete) operations on student records through an interactive web interface:

1. **Add a Student** — Register a new student with their name, age, department, and email.
2. **View All Students** — Display all registered students in a clean interactive table.
3. **Search for a Student** — Retrieve a specific student's details using their unique ID.
4. **Update Student Details** — Modify an existing student's name, age, department, or email.
5. **Delete a Student** — Remove a student record from the database by ID.

---

## 2. Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3 | Core programming language |
| **Backend API** | FastAPI | High-performance REST API framework |
| **ASGI Server** | Uvicorn | Runs the FastAPI backend server |
| **Data Validation** | Pydantic | Validates incoming requests and serializes responses |
| **Database** | SQLite | Lightweight file-based relational database (`students.db`) |
| **ORM** | SQLAlchemy | Maps Python classes to SQLite database tables |
| **Frontend UI** | Streamlit | Interactive web UI built purely in Python |
| **HTTP Client** | Requests | Sends HTTP requests from Streamlit to FastAPI |

---

## 3. Project Structure

```text
student-management/
│
├── backend/
│   ├── main.py          # FastAPI app initialization and API route endpoints
│   ├── database.py      # SQLite connection, SQLAlchemy engine, and session setup
│   ├── models.py        # SQLAlchemy database table definition (Student model)
│   ├── schemas.py       # Pydantic schemas for request/response validation
│   └── crud.py          # Database helper functions (Create, Read, Update, Delete)
│
├── frontend/
│   └── app.py           # Streamlit user interface
│
├── requirements.txt     # Required Python packages
├── README.md            # Project documentation
└── .gitignore           # Ignored files (virtualenv, __pycache__, *.db)
```

---

## 4. How to Install Dependencies

1. Open a terminal in the project root directory.
2. (Optional) Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install all required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. How to Run FastAPI (Backend)

From the project root directory, run:

```bash
uvicorn backend.main:app --reload
```

*(On Windows PowerShell, if `uvicorn` is not recognized in your current terminal session, run:)*
```bash
python -m uvicorn backend.main:app --reload
```

- **Backend API Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger UI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Keep this terminal window running while you start the frontend.

---

## 6. How to Run Streamlit (Frontend)

Open a **second terminal window** in the project root directory and run:

```bash
streamlit run frontend/app.py
```

*(On Windows PowerShell, if `streamlit` is not recognized in your current terminal session, run:)*
```bash
python -m streamlit run frontend/app.py
```

- **Streamlit Web App URL:** [http://localhost:8501](http://localhost:8501)

---

## 7. API Endpoints

| HTTP Method | Endpoint | Description | Request Body (JSON) | Success Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/students` | Return a list of all students | *None* | `200 OK` |
| `GET` | `/students/{student_id}` | Return a single student by ID | *None* | `200 OK` |
| `POST` | `/students` | Create a new student | `{"name", "age", "department", "email"}` | `201 Created` |
| `PUT` | `/students/{student_id}` | Update an existing student by ID | `{"name", "age", "department", "email"}` | `200 OK` |
| `DELETE` | `/students/{student_id}` | Delete a student by ID | *None* | `200 OK` |

### Example JSON Request Body (`POST /students` or `PUT /students/{student_id}`)

```json
{
  "name": "Alice Johnson",
  "age": 20,
  "department": "Computer Science",
  "email": "alice.johnson@example.com"
}
```

### Example JSON Response

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "age": 20,
  "department": "Computer Science",
  "email": "alice.johnson@example.com"
}
```

---

## 8. How FastAPI and Streamlit Communicate

The frontend and backend run as two separate processes and communicate over HTTP using JSON:

```text
+------------------------+          HTTP Request (JSON)           +------------------------+
|                        |  ----------------------------------->  |                        |
|   Streamlit Frontend   |     POST / GET / PUT / DELETE          |    FastAPI Backend     |
|   (frontend/app.py)    |     via Python `requests` library      |   (backend/main.py)    |
|   Port: 8501           |  <-----------------------------------  |   Port: 8000           |
+------------------------+          HTTP Response (JSON)          +------------------------+
                                                                              |
                                                                              | SQLAlchemy ORM
                                                                              v
                                                                  +------------------------+
                                                                  |    SQLite Database     |
                                                                  |     (students.db)      |
                                                                  +------------------------+
```

1. **User Interaction**: The user fills out a form or clicks a button in the Streamlit UI (`frontend/app.py`).
2. **HTTP Request**: Streamlit uses the `requests` library (`requests.get`, `requests.post`, `requests.put`, `requests.delete`) to call the FastAPI server at `http://127.0.0.1:8000`.
3. **Validation & Database Operation**: FastAPI validates the request data using **Pydantic** (`schemas.py`), executes the database operation via **SQLAlchemy** (`crud.py` & `models.py`), and saves changes to `students.db`.
4. **HTTP Response**: FastAPI returns a JSON response with an HTTP status code (`200`, `201`, `400`, `404`, or `422`), which Streamlit displays using `st.success()`, `st.error()`, or `st.dataframe()`.

---

## 9. UI Preview / Placeholders

### Sidebar Navigation & Add Student Page
```text
+----------------------+---------------------------------------------------+
| Navigation           | 🎓 Student Management System                      |
| [ Add Student    v ] |                                                   |
|                      | Add a New Student                                 |
|                      | Name:       [ Alice Johnson                     ] |
|                      | Age:        [ 20                              ] |
|                      | Department: [ Computer Science                v ] |
|                      | Email:      [ alice.johnson@example.com         ] |
|                      |                                                   |
|                      | [ Add Student ]                                   |
|                      |                                                   |
|                      | ✅ Student 'Alice Johnson' added with ID 1!       |
+----------------------+---------------------------------------------------+
```

### View Students Page
```text
+----------------------+---------------------------------------------------+
| Navigation           | 🎓 Student Management System                      |
| [ View Students  v ] |                                                   |
|                      | All Registered Students                           |
|                      | [ Refresh List ]                                  |
|                      | +----+---------------+-----+------------------+   |
|                      | | id | name          | age | department       |   |
|                      | +----+---------------+-----+------------------+   |
|                      | | 1  | Alice Johnson | 20  | Computer Science |   |
|                      | +----+---------------+-----+------------------+   |
+----------------------+---------------------------------------------------+
```
