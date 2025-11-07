# Blue Archive Gacha Simulator (Alternative Implementations)

> **⚠️ Disclaimer**
>
> This is a fan-made, non-profit hobby project created purely for fun and educational purposes. There is no commercial benefit associated with this project. It is not affiliated with, authorized, or endorsed by Nexon Games, Yostar, or their affiliates in any way. All characters, images, and other intellectual property from Blue Archive are trademarks and copyrights of their respective owners.

## 🎯 Project Goal

This repository serves as a personal case study to explore and compare different web development stacks. The goal is to rebuild the same application with various tools to understand their unique architectures, complexities, and advantages.

This project was originally developed as a full-stack application using Django and server-side rendering.

**[➡️ View the Original Django Version Here](https://github.com/catptype/Blue-Archive-Gacha-Simulator-V2)**

---

## 🧪 Implementation 1: FastAPI + Vue.js

This version refactors the application into a modern decoupled architecture, with a dedicated backend API serving a dynamic Single Page Application (SPA) frontend.

### 🛠️ Tech Stack

*   **Backend:** FastAPI, Python, SQLAlchemy, SQLAdmin, JWT (for authentication)
*   **Frontend:** Vue.js, TypeScript, Tailwind CSS
*   **Database:** SQLite
*   **Data Visualization:** ApexCharts

### ✨ Key Architectural Differences from the Django Version

This implementation isn't just a change of frameworks; it's a fundamental shift in architecture.

*   **Decoupled Architecture:** Unlike the original monolithic Django app, this version separates concerns completely. The FastAPI server exposes a RESTful API, and the Vue.js frontend acts as a pure consumer of that API.
*   **Asynchronous Backend:** Leverages FastAPI's asynchronous capabilities for high-performance API endpoints, which is a key area of exploration compared to Django's traditional synchronous request/response cycle.
*   **Client-Side State Management:** All UI state, user data, and gacha results are managed directly within the Vue.js application (using tools like Pinia or Vue's built-in reactivity), creating a fluid user experience without full page reloads.
*   **Static Site Serving:** The frontend is a standalone static application that can be served from any simple web server or CDN, communicating with the backend API independently.

### 📸 Screenshots

The user interface and core features are designed to replicate the original project. For screenshots of the UI, please refer to the [original repository's README](https://github.com/catptype/Blue-Archive-Gacha-Simulator-V2#screenshots).

---

## 🚀 Getting Started

To run this project, you will need to run two separate processes in two terminals: one for the backend API and one for the frontend application.

### 1. Backend Setup (FastAPI)

1.  **Navigate to the backend directory** from the project root:
    ```sh
    cd backend_fastapi
    ```
2.  **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3.  **Initialize the database and create an admin user.** Run these commands from the project's *root* directory:
    ```sh
    # Create the database and tables
    python -m backend_fastapi.create_db

    # Create a superuser (replace with your desired credentials)
    python -m backend_fastapi.create_superuser your_username your_password
    ```
4.  **Run the development server:**
    ```sh
    uvicorn backend_fastapi.main:app --reload
    ```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup (Vue.js)

1.  **Navigate to the frontend directory** from the project root:
    ```sh
    cd frontend_vue
    ```
2.  **Install Node.js dependencies:**
    ```sh
    npm install
    npm run dev
    ```
The application will be available at `http://localhost:5173/` (or whichever port Vite specifies).

---

## 📄 Resources

The visual assets and fonts used in this project were sourced from the following excellent community resources.

*   [Student Images Asset](https://bluearchive.wiki/wiki/Characters): Source for student character portraits and artworks.
*   [Web Logo Generator](https://tmp.nulla.top/ba-logo/): A tool for generating web logos related to Blue Archive.
*   [RoGSanSrfStd-Bd Font](https://www.ffonts.net/RoGSanSrfStd-Bd.font): The font used in the project for a specific style or branding.