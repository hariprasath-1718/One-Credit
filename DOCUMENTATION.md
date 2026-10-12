# STUDENT MANAGEMENT SYSTEM
### Simple Web-Based Student Information and CRUD Management System
**Mini Project – 1 Credit**

---

## 1. Abstract
The **Student Management System** is a full-stack, web-based academic application designed to digitize and simplify student record administration. The system enables academic administrators and faculty to perform end-to-end **CRUD** (Create, Read, Update, Delete) operations on student profiles, ensuring data accuracy and easy retrieval. The application is built using a decoupled architecture with **Streamlit** delivering an intuitive, modern user interface and **FastAPI** providing a high-performance RESTful API backend. **SQLite** paired with **SQLAlchemy ORM** is used for persistent local data storage, and **Pydantic** enforces strict schema validation. The project demonstrates how lightweight Python-powered technologies can work seamlessly together to deliver a reliable, service-oriented institutional application.

---

## 2. Problem Statement
Academic institutions frequently rely on manual record-keeping, disjointed spreadsheets, or cumbersome legacy systems to maintain student information. These traditional practices are prone to human error, duplicate data entries, unauthorized modifications, and slow record retrieval. A centralized, digital student management assistant eliminates these inefficiencies by providing structured data entry, real-time validation (such as duplicate email prevention), instant ID-based lookups, and clear record maintenance in a single unified interface.

---

## 3. Objectives
- **Develop a Web-Based Application**: Build an accessible, responsive interface for administering student records.
- **Implement Complete CRUD Operations**: Provide seamless functionality to add, view, search, modify, and delete student data.
- **Enforce Strict Data Validation**: Utilize Pydantic models and database constraints to ensure unique emails, positive IDs, and valid age ranges.
- **Decoupled API Architecture**: Design clean RESTful endpoints using FastAPI with clear request/response models.
- **Persistent Data Management**: Integrate SQLite and SQLAlchemy ORM for lightweight, file-based relational data handling.
- **Interactive Documentation**: Provide automated Swagger UI and ReDoc specifications for API exploration and testing.

---

## 4. Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language for backend and frontend logic |
| **FastAPI** | High-performance backend REST API framework |
| **Streamlit** | Interactive, modern web user interface |
| **SQLite** | Lightweight, file-based relational database (`students.db`) |
| **SQLAlchemy** | Object Relational Mapper (ORM) for database models and session handling |
| **Pydantic** | Schema definition, data parsing, and input/output validation |
| **Requests** | HTTP client library for communication between Streamlit and FastAPI |
| **Uvicorn** | Asynchronous Server Gateway Interface (ASGI) server running FastAPI |

---

## 5. System Architecture
The application follows a clean **three-layer architecture** separating presentation, business logic, and data persistence:

1. **Presentation Layer (Streamlit)**: Collects user inputs, renders responsive tables, statistics, and handles interactive notifications.
2. **API & Business Logic Layer (FastAPI)**: Validates incoming HTTP requests, enforces business rules (e.g., verifying email uniqueness), and invokes CRUD functions.
3. **Data Layer (SQLAlchemy & SQLite)**: Maps object models to the relational schema and performs database queries on `students.db`.

$$\text{User} \longrightarrow \text{Streamlit Frontend} \xrightarrow{\text{HTTP / REST}} \text{FastAPI Backend} \longrightarrow \text{CRUD Logic / SQLAlchemy} \longrightarrow \text{SQLite Database}$$

---

## 6. Main Features
- **Interactive Dashboard**: Overview cards displaying total students, department counts, and quick system status.
- **Student Enrollment (Create)**: Simple form to register new students with instant email duplication checks.
- **Directory & Filter (Read All)**: Comprehensive tabular view of all registered students with department-wise filtering.
- **Targeted Lookup (Search)**: Retrieve individual student profiles by entering their unique Student ID.
- **Profile Modification (Update)**: Edit student details (name, age, department, email) with conflict safeguards.
- **Record Removal (Delete)**: Delete obsolete student entries with validation.
- **Interactive API Documentation**: Live Swagger UI accessible at `/docs` and ReDoc at `/redoc`.
- **Automatic Schema Initialization**: Auto-creates SQLite tables on application startup.
- **Informative Status Feedback**: Detailed HTTP error responses (201 Created, 400 Bad Request, 404 Not Found, 422 Unprocessable Entity).

---

## 7. Database Schema & Core Entities
The primary entity managed by the system is the **Student** record, defined using SQLAlchemy:

| Field | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Autoincrement, Index | Unique student identifier |
| `name` | String(100) | Not Null | Full legal name of the student |
| `age` | Integer | Not Null, $15 \le \text{age} \le 100$ | Age of the student |
| `department` | String(100) | Not Null | Academic department (e.g., CSE, ECE, MECH) |
| `email` | String(100) | Unique, Not Null, Index | Student institutional or personal email |

### Supported Operations:
- `create_student`: Adds a new student record to the database.
- `get_all_students`: Retrieves all active student entries.
- `get_student_by_id`: Fetches a single record using the unique integer ID.
- `get_student_by_email`: Searches for an existing student by email to prevent duplicates.
- `update_student`: Modifies existing fields while guarding against email conflicts.
- `delete_student`: Permanently removes the selected record.

---

## 8. FastAPI Endpoints

| Method | Endpoint | Purpose | Status Code |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Root health-check endpoint confirming backend availability | `200 OK` |
| **GET** | `/students` | Retrieves list of all registered student records | `200 OK` |
| **GET** | `/students/{student_id}` | Retrieves details of a specific student by ID | `200 OK` / `404 Not Found` |
| **POST** | `/students` | Registers a new student; checks for duplicate email | `201 Created` / `400 Bad Request` |
| **PUT** | `/students/{student_id}` | Updates existing student attributes by ID | `200 OK` / `404 Not Found` / `400 Bad Request` |
| **DELETE** | `/students/{student_id}` | Removes a student record by ID | `200 OK` / `404 Not Found` |

---

## 9. Working of the System
1. The user opens the **Streamlit web application** in their browser.
2. The user navigates to the desired section (Dashboard, Add Student, View All, Search, Update, or Delete).
3. When registering a student, the user enters the name, age, department, and email address.
4. Streamlit sends an HTTP `POST` request with the JSON payload to the FastAPI `/students` endpoint.
5. FastAPI verifies the payload structure against the `StudentCreate` Pydantic schema.
6. The CRUD layer checks SQLite via SQLAlchemy to verify that the email address is not already registered.
7. If validated, the record is inserted into `students.db`, and a `201 Created` response with the new student's ID is returned.
8. Streamlit displays a success confirmation badge, and the student immediately appears in the directory table.

---

## 10. Testing and Results
The application was thoroughly verified using both the Streamlit web interface and FastAPI's interactive Swagger documentation (`/docs`). All core endpoints and data integrity rules passed testing:

| Test Case | Expected Result | Status |
| :--- | :--- | :--- |
| **Root Health Check** | API returns `{"message": "Welcome to the Student Management System API"}` | **Passed** |
| **Valid Student Registration** | New student is created with autoincremented ID; returns status `201` | **Passed** |
| **Duplicate Email Prevention** | Attempting to register an existing email returns status `400 Bad Request` | **Passed** |
| **Retrieve All Students** | Returns complete JSON array of student records with status `200 OK` | **Passed** |
| **Search by Valid ID** | Returns student record matching the specified ID | **Passed** |
| **Search by Invalid ID** | Returns status `404 Not Found` with appropriate error message | **Passed** |
| **Update Student Details** | Modifies specified fields and saves updated record; returns status `200` | **Passed** |
| **Delete Student Record** | Deletes record from SQLite; returns success confirmation message | **Passed** |
| **Interactive Swagger Docs** | All schemas and endpoints are visible, documented, and testable at `/docs` | **Passed** |

---

## 11. Advantages
- **Intuitive User Interface**: Streamlit provides a clean, user-friendly UI without needing complex HTML/JavaScript setup.
- **High Performance**: FastAPI offers asynchronous request handling with fast execution speeds.
- **Robust Data Integrity**: Pydantic and SQLAlchemy prevent bad data, type mismatches, and duplicate records.
- **Zero-Configuration Database**: SQLite requires no dedicated server installation or connection credentials.
- **Clear Architectural Separation**: The frontend, API layer, database models, and CRUD queries are cleanly organized into modular files.
- **Self-Documenting API**: Automatic OpenAPI/Swagger documentation simplifies debugging and external integration.

---

## 12. Limitations
- **Single-Host Database**: SQLite is a file-based database, which is ideal for single-node academic prototypes but not suited for high-concurrency multi-server distributed environments.
- **Authentication**: The initial version does not implement multi-role authentication (Admin vs. Student login).
- **Batch Processing**: Student records must currently be added individually rather than via bulk Excel/CSV file upload.

---

## 13. Future Enhancements
- **User Authentication & Role-Based Access (RBAC)**: Introduce JWT-based authentication distinguishing between Admin, Faculty, and Student roles.
- **Bulk CSV / Excel Import & Export**: Allow administrators to import or export entire batches of student records in one click.
- **Academic Course & Grade Tracking**: Extend the schema to link students to enrolled subjects, attendance, and semester GPAs.
- **Cloud Database Integration**: Transition from SQLite to PostgreSQL or MySQL for cloud deployments (e.g., AWS RDS, Supabase).
- **PDF Report Generation**: Automatically generate printable student profile summary sheets and academic transcripts.

---

## 14. Conclusion
The **Student Management System** successfully demonstrates a practical, end-to-end full-stack web application built using Python, FastAPI, Streamlit, and SQLite. By replacing manual paperwork with a centralized digital system, it provides seamless record creation, instant lookups, update capabilities, and deletion while enforcing relational integrity and API standards. The project serves as a comprehensive, modular foundation for academic administrative automation within a compact 1-credit mini-project scope.
