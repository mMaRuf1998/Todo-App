# 📝 Todo-App - Task Management System

Live: https://todo-app-final-tkky.onrender.com/

You can integrate mysql or postgresql. Just change database.py url.


A full-featured task management web application built with **FastAPI**. This project helps users organize, track, and manage their daily tasks with user authentication and role-based access control.

## ✨ Features

- ✅ Complete CRUD operations for tasks
- 🔐 User authentication & authorization (JWT tokens)
- 👑 Admin role with user management capabilities
- 🎨 User-friendly web interface with Jinja2 templating
- 📱 Responsive design with static files support
- 💾 SQLite database for lightweight storage
- 🔄 RESTful API endpoints for integration

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **Templating:** Jinja2
- **Database:** SQLite
- **Authentication:** JWT (JSON Web Tokens) + Bcrypt password hashing
- **Frontend:** HTML, CSS, JavaScript
- **Server:** Uvicorn (ASGI)
- **ORM:** SQLAlchemy

## 📁 Project Structure

```text
Todo-App/
├── TodoApp/                  # Main application folder
│   ├── main.py               # Application entry point
│   ├── database.py           # Database configuration
│   ├── models.py             # SQLAlchemy database models
│   ├── routers/              # API route handlers
│   │   ├── auth.py           # Authentication routes
│   │   ├── todos.py          # Todo CRUD operations
│   │   ├── admin.py          # Admin-only routes
│   │   └── users.py          # User profile routes
│   ├── templates/            # Jinja2 HTML templates
│   ├── static/               # CSS, JavaScript files
│   └── todosapp.db           # SQLite database file
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mMaRuf1998/Todo-App.git
   cd Todo-App
   ```

2. **Navigate to the project folder**
   ```bash
   cd TodoApp
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows Git Bash: source venv/Scripts/activate
   ```

4. **Install dependencies**
   ```bash
   pip install fastapi uvicorn jinja2 sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart
   ```

5. **Set up environment variables**
   Create a `.env` file in the `TodoApp` directory with:
   ```text
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   DB_PASS=your-db-password (optional for SQLite)
   ```

6. **Run the application**
   ```bash
   uvicorn TodoApp.main:app --reload
   ```
   Open your browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📡 API Endpoints

### Authentication Routes (`/auth`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/auth/registration-page` | User registration form (HTML) |
| `GET` | `/auth/login-page` | User login form (HTML) |
| `POST` | `/auth/` | Create a new user account |
| `POST` | `/auth/token` | Login and get access token |

### Todo Routes (`/todos`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/todos/` | Get all todos for logged-in user (JSON) |
| `GET` | `/todos/todo-page` | View all todos web page (HTML) |
| `GET` | `/todos/add-todo-page` | Add new todo form (HTML) |
| `GET` | `/todos/edit-todo-page/{todo_id}` | Edit todo form (HTML) |
| `GET` | `/todos/{todo_id}` | Get a specific todo by ID (JSON) |
| `POST` | `/todos/create` | Create a new todo |
| `PUT` | `/todos/{todo_id}` | Update a todo |
| `DELETE` | `/todos/{todo_id}` | Delete a todo |

### Admin Routes (`/admin`) - Admin only

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/admin/todos` | Get all todos from all users (JSON) |
| `DELETE` | `/admin/todos/{todo_id}` | Delete any todo by ID |

### User Routes (`/user`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/user/` | Get current user information |
| `PUT` | `/user/changepassword` | Change user password |
| `PUT` | `/user/phonenumber/{phonenumber}` | Update user's phone number |

### General Routes

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Redirects to `/todos/todo-page` |
| `GET` | `/healthy` | Health check endpoint |

### Interactive API Documentation

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🔐 Authentication

Most endpoints require a valid JWT token. To authenticate:
1. Register a new user at `/auth/registration-page`
2. Login at `/auth/login-page` or use the `/auth/token` endpoint
3. Include the token in requests:
   - **Header:** `Authorization: Bearer your-access-token`
   - **Cookie:** The web interface stores the token in cookies automatically

### User Roles
- **Regular User:** Can manage their own todos only
- **Admin:** Can view and delete all users' todos via `/admin` routes

## 💾 Database

This project uses SQLite as the database. The database file (`todosapp.db`) will be automatically created when you first run the application. No additional setup is required.

### Database Schema
- **Users table:** Stores user information (id, email, username, hashed_password, role, etc.)
- **Todos table:** Stores tasks (id, title, description, priority, complete status, owner_id)

## 📝 Todo Object Structure

```json
{
  "title": "string (1-100 characters)",
  "description": "string (1-100 characters)",
  "priority": "integer (1-5)",
  "complete": "boolean (default: false)"
}
```
