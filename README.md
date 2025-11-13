# Blue Archive Gacha Simulator (Alternative Implementations)

> **⚠️ Disclaimer**
>
> This is a fan-made, non-profit hobby project created purely for fun and educational purposes. There is no commercial benefit associated with this project. It is not affiliated with, authorized, or endorsed by Nexon Games, Yostar, or their affiliates in any way. All characters, images, and other intellectual property from Blue Archive are trademarks and copyrights of their respective owners.

## 🎯 Project Goal

This repository serves as a personal case study to explore and compare different web development stacks. The goal is to rebuild the same application with various tools to understand their unique architectures, complexities, and advantages.

This project was originally developed as a full-stack application using Django and server-side rendering.

**[➡️ View the Original Django Version Here](https://github.com/catptype/Blue-Archive-Gacha-Simulator-V2)**

## 🏛️ Architectural Philosophy

All modern implementations in this repository follow a **decoupled, API-driven architecture**.

*   **Backend's Role:** To provide a stateless, JSON-based API. It is responsible for business logic, database interaction, and authentication.
*   **Frontend's Role:** To act as a pure consumer of the API. It is a standalone Single Page Application (SPA) responsible for all UI, rendering, and client-side state management.

This separation allows any implemented frontend to work with any implemented backend, providing a flexible platform for comparison.

---

## ⚙️ Implemented Backends

This section details the available backend API servers.

### 🐍 Backend 1: FastAPI

A high-performance, asynchronous Python web framework ideal for building robust APIs.

#### Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework** | FastAPI |
| **ORM** | SQLAlchemy |
| **Database** | SQLite |
| **Admin Panel**| SQLAdmin |
| **Auth** | JWT with `python-jose` |
| **Validation** | Pydantic |

#### Key Features

*   **Asynchronous by Design:** Leverages Python's `async` and `await` for non-blocking, high-performance I/O.
*   **Data Validation:** Uses Pydantic for strict, type-hinted data validation and serialization, creating a reliable API contract.
*   **Automatic Docs:** Generates interactive OpenAPI (Swagger UI) and ReDoc documentation automatically.
*   **Secure Admin Panel:** Integrates SQLAdmin to provide a secure, superuser-only interface for database management, mimicking the Django Admin.

#### Getting Started (FastAPI)

1.  Navigate to the backend directory: `cd backend_fastapi`
2.  Set up and activate a Python virtual environment (e.g., Conda).
3.  Install dependencies: `pip install -r requirements.txt`
4.  Initialize the database (from the project **root**): `python -m backend_fastapi.create_db`
5.  Create a superuser (from the project **root**): `python -m backend_fastapi.create_superuser <username> <password>`
6.  Run the server: `uvicorn backend_fastapi.main:app --reload`

---

## 🎨 Implemented Frontends

This section details the available frontend SPA clients.

### 🖼️ Frontend 1: Vue.js

A progressive, component-based JavaScript framework for building modern, reactive user interfaces.

#### Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework** | Vue.js 3 (with Composition API) |
| **Build Tool** | Vite |
| **Language** | TypeScript |
| **State Mngmt**| Pinia |
| **Styling** | Tailwind CSS |
| **Data Viz** | ApexCharts |

#### Key Features

*   **Component-Based:** The entire UI is broken down into small, reusable, and self-contained `.vue` components.
*   **Declarative & Reactive:** Manages UI state with the Composition API. The DOM automatically "reacts" to data changes, eliminating manual DOM manipulation.
*   **Centralized State:** Uses Pinia to globally manage application-wide state, such as user authentication and toast notifications.
*   **Fast Development:** Leverages Vite for an extremely fast development server with Hot Module Replacement (HMR).

#### Getting Started (Vue.js)

1.  Navigate to the frontend directory: `cd frontend_vue`
2.  Create a local environment file (`.env.development`) and add the backend API URL:
    ```
    VITE_API_BASE_URL=http://127.0.0.1:8000
    ```
3.  Install dependencies: `npm install`
4.  Run the development server: `npm run dev`

---

## 🚀 Running the Project

To run the application, you must have **one backend** and **one frontend** running simultaneously in two separate terminals.

1.  **Terminal 1 (Backend):** Follow the "Getting Started" steps for your chosen backend (e.g., FastAPI).
2.  **Terminal 2 (Frontend):** Follow the "Getting Started" steps for your chosen frontend (e.g., Vue.js).
3.  **Access:** Open your browser to the URL provided by the frontend's development server (typically `http://localhost:5173`).