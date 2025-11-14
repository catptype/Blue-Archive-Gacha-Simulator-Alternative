# Blue Archive Gacha Simulator (Alternative Implementations)

> **⚠️ Disclaimer**
>
> This is a fan-made, non-profit hobby project created purely for fun and educational purposes. There is no commercial benefit associated with this project. It is not affiliated with, authorized, or endorsed by Nexon Games, Yostar, or their affiliates in any way. All characters, images, and other intellectual property from Blue Archive are trademarks and copyrights of their respective owners.

## 🎯 Project Goal

This repository serves as a personal case study to explore and compare different web development stacks. The goal is to rebuild the same application with various tools to understand their unique architectures, complexities, and advantages.

This project was originally developed as a full-stack application using Django and server-side rendering. This repository documents the journey of re-implementing it with new technologies.

**[➡️ View the Original Django Version Here](https://github.com/catptype/Blue-Archive-Gacha-Simulator-V2)**

## 🏛️ Architectural Philosophy

All modern implementations in this repository follow a **decoupled, API-driven architecture**.

*   **Backend's Role:** To provide a stateless, JSON-based API. It is responsible for logic, database interaction, and authentication.
*   **Frontend's Role:** To act as a pure consumer of the API. It is a standalone Single Page Application (SPA) responsible for all UI, rendering, and client-side state management.

This separation allows any implemented frontend to work with any implemented backend, providing a flexible platform for comparison.

---

## ⚙️ Implemented Backends

This section details the available backend API servers.

### 🐍 Backend 1: FastAPI

A high-performance, asynchronous Python web framework ideal for building robust APIs.

#### Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | FastAPI | Core asynchronous web framework for building the API endpoints. |
| **Database / ORM** | SQLAlchemy | The primary Object-Relational Mapper for all database interactions. |
| **Databases** | **PostgreSQL, MySQL, MariaDB** | **Production-ready**, robust relational databases. |
| **^^** | **SQLite** | **Development-only**, simple file-based database for easy setup. |
| **Authentication** | `bcrypt` & `python-jose` | For secure password hashing and JWT-based session management. |
| **Admin Panel** | SQLAdmin | Provides a secure, auto-generated web UI for database management. |
| **Data Validation** | Pydantic | Used for all data validation, serialization, and defining API schemas. |
| **Caching** | Redis / In-Memory | A swappable caching layer for production and development. |
| **Dev Server** | Uvicorn | High-performance ASGI server used for local development (`--reload`). |
| **Prod Server** | Gunicorn | Battle-tested process manager for running Uvicorn workers in production. |

#### Getting Started (FastAPI)

For local development, this project defaults to using **SQLite**.

1.  Navigate to the backend directory: `cd backend_fastapi`
2.  Set up and activate a Python virtual environment (e.g., Conda).
3.  Install dependencies: `pip install -r requirements.txt`
4.  Initialize the database (from the project **root**): `python -m backend_fastapi.create_db`
5.  Create a superuser (from the project **root**): `python -m backend_fastapi.create_superuser <username> <password>`
6.  Run the server:
    ```sh
    # Set the LOG_LEVEL environment variable to see detailed debug messages
    # On Windows (PowerShell): $env:LOG_LEVEL="DEBUG"
    # On Linux/macOS: export LOG_LEVEL=DEBUG
    uvicorn backend_fastapi.main:app --reload
    ```

---

## 🎨 Implemented Frontends

This section details the available frontend SPA clients.

### 🖼️ Frontend 1: Vue.js

A progressive, component-based JavaScript framework for building modern, reactive user interfaces.

#### Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | Vue.js 3 (Composition API) | For building a reactive, component-based user interface. |
| **Build Tool** | Vite | Next-generation frontend tooling for a fast development server and optimized builds. |
| **Language** | TypeScript | Adds static typing to JavaScript for a more robust and scalable codebase. |
| **Routing** | Vue Router | For all client-side routing in the Single Page Application. |
| **State Mngmt** | Pinia | For global state management (user authentication, toast notifications). |
| **Styling** | Tailwind CSS | A utility-first CSS framework for rapid, responsive UI design. |
| **API Client** | Axios | For making HTTP requests to the backend API. |
| **Data Viz** | ApexCharts | For creating modern, interactive charts on the user dashboard. |

#### Getting Started (Vue.js)

1.  Navigate to the frontend directory: `cd frontend_vue`
2.  Install dependencies: `npm install`
3.  Run the development server: `npm run dev`
    > The backend API URL is configured with a fallback in [`frontend_vue/src/config.ts`](frontend_vue/src/config.ts). For local development, it defaults correctly to `http://127.0.0.1:8000`.

---

## 🚀 Running the Project

To run the application, you must have **one backend** and **one frontend** running simultaneously in two separate terminals.

1.  **Terminal 1 (Backend):** Follow the "Getting Started" steps for your chosen backend (e.g., FastAPI).
2.  **Terminal 2 (Frontend):** Follow the "Getting Started" steps for your chosen frontend (e.g., Vue.js).
3.  **Access:** Open your browser to the URL provided by the frontend's development server (typically `http://localhost:5173`).

---

## 🐳 Production & Deployment with Docker

This project is fully configured for a containerized production deployment using Docker Compose.

### 1. Configure Your Deployment

The [`docker-compose.yml`](docker-compose.yml) file is a template that allows you to choose your database. By default, it is set to use **PostgreSQL**. To switch to MySQL or MariaDB:
1.  **Comment/Uncomment** the desired database service block in `docker-compose.yml`.
2.  **Update the `DATABASE_URL`** in the `backend` service's `environment` section to match your choice.
3.  **Update the volumes** at the bottom of the file to match your choice.
4.  Ensure the correct database driver (`psycopg2-binary` or `mysqlclient`) is installed in the `Dockerfile.backend_fastapi`.

### 2. Run the Application

Execute these commands from the project's **root directory**.

1.  **Build and Start Services:**
    This command builds the Docker images and starts the frontend, backend, database, and cache containers in the background.
    ```sh
    docker compose up --build -d
    ```
2.  **Initialize the Database (Run Once):**
    This command runs a temporary container to create the database schema and seed it with initial data.
    ```sh
    docker compose run --rm backend python -m backend_fastapi.create_db
    ```
3.  **Create a Superuser (Run Once):**
    This command runs a temporary container to create your administrative user.
    ```sh
    docker compose run --rm backend python -m backend_fastapi.create_superuser your_admin_name your_password
    ```

### 3. Access the Deployed Application

*   **Frontend Application:** `http://localhost:5173`
*   **Backend Admin Panel:** `http://localhost:8000/admin`

To stop all running services, use `docker compose down`.

---

## 🔮 Future Implementations

This project is an ongoing exploration. Future plans include re-implementing the frontend and/or backend with other exciting technologies to continue the learning and comparison process. Potential candidates include:

*   **Frontend:**
    *   React
*   **Backend:**
    *   Golang