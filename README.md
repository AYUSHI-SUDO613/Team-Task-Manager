# Team Task Manager

Team Task Manager is a full-stack web application designed for teams to create projects, assign tasks, and track progress effectively. Inspired by industry-leading tools like Trello and Asana, it offers a clean, modern, and professional UI.

## Features

- **Authentication System:** Secure user registration, login, and session management.
- **Role-Based Access Control (RBAC):** 
  - **Admin:** Full control over project and task management, including adding members.
  - **Member:** Can view projects, tasks, and update the status of tasks.
- **Dashboard:** Visual overview of task statistics including total, completed, pending, and overdue tasks.
- **Project Management:** Create new projects and manage team members.
- **Task Management:** Interactive Kanban-style board to track tasks across "To Do", "In Progress", and "Done" statuses.
- **API Backend:** Powered by Django REST Framework for dynamic interactions.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** Django Templates, Bootstrap 5, Vanilla JS, Custom CSS
- **Database:** SQLite (development) / PostgreSQL (production ready)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd team-task-manager
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://localhost:8000` to view the application.

## Deployment on Railway

This application is ready to be deployed on Railway.

1. Create a new project on Railway.
2. Link your GitHub repository.
3. Add the following environment variables in the Railway dashboard:
   - `SECRET_KEY`: A strong secret key.
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*` (or your Railway domain)
   - `DATABASE_URL`: Add a PostgreSQL database to your Railway project and use its connection string.
4. Railway will automatically detect the `Procfile`, `requirements.txt`, and `runtime.txt` to deploy the Django app.
