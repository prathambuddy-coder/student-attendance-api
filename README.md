# Student Attendance Management System

A RESTful Student Attendance Management API built using Flask and MySQL.

This project provides APIs for managing students, subjects, attendance records, and user authentication. It also supports attendance filtering and calculates both overall and subject-wise attendance percentages.

## Features

- User registration and login
- Secure password hashing
- Student CRUD operations
- Subject CRUD operations
- Mark student attendance
- View attendance records
- Filter attendance by student, subject, and date
- Overall attendance percentage
- Subject-wise attendance percentage
- MySQL database integration
- Flask Blueprint architecture
- RESTful API endpoints
- Centralized error handling

## Tech Stack

- Python
- Flask
- MySQL
- mysql-connector-python
- Werkzeug
- Flask-CORS
- python-dotenv
- REST API

## Project Structure

```text
student_attendance/
│
├── auth/
│   ├── __init__.py
│   └── auth_routes.py
│
├── routes/
│   ├── __init__.py
│   ├── student_routes.py
│   ├── subject_routes.py
│   └── attendance_routes.py
│
├── .env
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── db.py
└── requirements.txt

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login user |

### Students

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Add a new student |
| GET | `/students` | Get all students |
| GET | `/students/<id>` | Get student by ID |
| PUT | `/students/<id>` | Update student |
| DELETE | `/students/<id>` | Delete student |

### Subjects

| Method | Endpoint | Description |
|---|---|---|
| POST | `/subjects` | Add a new subject |
| GET | `/subjects` | Get all subjects |
| GET | `/subjects/<id>` | Get subject by ID |
| PUT | `/subjects/<id>` | Update subject |
| DELETE | `/subjects/<id>` | Delete subject |

### Attendance

| Method | Endpoint | Description |
|---|---|---|
| POST | `/attendance` | Mark attendance |
| GET | `/attendance` | Get attendance records |
| GET | `/attendance?student_id=<id>` | Filter by student |
| GET | `/attendance?subject_id=<id>` | Filter by subject |
| GET | `/attendance?date=<date>` | Filter by date |
| GET | `/attendance/report/<student_id>` | Get overall attendance report |
| GET | `/attendance/report/<student_id>?subject_id=<id>` | Get subject-wise attendance report |

## Database Structure

The project uses MySQL with four main tables.

### Users

Stores authentication details.

| Column | Description |
|---|---|
| `id` | Primary key |
| `username` | Unique username |
| `password` | Hashed password |

### Students

Stores student information.

| Column | Description |
|---|---|
| `id` | Primary key |
| `name` | Student name |
| `age` | Student age |
| `branch` | Student branch |
| `email` | Student email |

### Subjects

Stores subject information.

| Column | Description |
|---|---|
| `id` | Primary key |
| `name` | Subject name |
| `code` | Subject code |

### Attendance

Stores attendance records.

| Column | Description |
|---|---|
| `id` | Primary key |
| `student_id` | Foreign key referencing students |
| `subject_id` | Foreign key referencing subjects |
| `date` | Attendance date |
| `status` | `Present` or `Absent` |

### Relationships

```text
Students
   │
   │ 1
   │
   │ N
Attendance
   │
   │ N
   │
   │ 1
Subjects
```

## Example API Requests

### Register User

**POST** `/register`

```json
{
    "username": "pratham",
    "password": "hello123"
}
```

### Login

**POST** `/login`

```json
{
    "username": "pratham",
    "password": "hello123"
}
```

### Add Student

**POST** `/students`

```json
{
    "name": "Pratham",
    "age": 19,
    "branch": "AIML",
    "email": "pratham@example.com"
}
```

### Add Subject

**POST** `/subjects`

```json
{
    "name": "Data Structures",
    "code": "DSA"
}
```

### Mark Attendance

**POST** `/attendance`

```json
{
    "student_id": 1,
    "subject_id": 1,
    "date": "2026-08-24",
    "status": "Present"
}
```

### Get Attendance

**GET** `/attendance`

Returns attendance records along with student and subject names.

### Filter Attendance

**GET** `/attendance?student_id=1`

**GET** `/attendance?subject_id=1`

**GET** `/attendance?date=2026-08-24`

Filters can also be combined:

**GET** `/attendance?student_id=1&subject_id=1`

### Overall Attendance Report

**GET** `/attendance/report/1`

Returns the student's total classes, present classes, absent classes, and attendance percentage.

### Subject-wise Attendance Report

**GET** `/attendance/report/1?subject_id=1`

Returns attendance statistics for a specific student and subject.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prathambuddy-coder/student-attendance-api.git
cd student-attendance-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as a reference:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=student_attendance
```

Replace `your_password` with your actual MySQL password.

### 5. Set Up the MySQL Database

Create the `student_attendance` database in MySQL and create the required tables:

- `users`
- `students`
- `subjects`
- `attendance`

### 6. Run the Application

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## HTTP Status Codes

The API uses standard HTTP status codes:

| Status Code | Meaning |
|---|---|
| `200` | Request successful |
| `201` | Resource created successfully |
| `400` | Invalid or missing request data |
| `401` | Authentication failed |
| `404` | Resource not found |
| `500` | Internal server error |

## Future Improvements

- JWT-based authentication
- Role-based access control
- Frontend attendance dashboard
- Attendance alerts for low attendance
- Export attendance reports to Excel/PDF
- Pagination for large datasets
- Swagger/OpenAPI documentation

## Author

**Pratham Wankhade**

Student developer interested in Python, Flask, SQL, and software development.