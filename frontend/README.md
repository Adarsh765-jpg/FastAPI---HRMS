# HRMS Frontend Dashboard

A modern, professional React-based dashboard for the Employee Management System. Built with Vite and Vanilla CSS for a clean, corporate aesthetic.

## 🚀 Features

- **Role-Based UI:**
  - **Admin:** Full access to all features.
  - **HR:** Restricted "Add Employee" form (Role locked to Employee).
  - **Employee:** Read-only view (No Add/Edit buttons).
- **Authentication:** Secure login with JWT storage and auto-redirects.
- **Route Protection:** Protected routes prevent unauthorized access to Admin/HR pages.
- **Employee Management:**
  - List view with Pagination.
  - Search & Filter by Department/Role.
  - Add/Edit Employee forms.

## 🛠️ Tech Stack

- **Framework:** React (Vite)
- **Styling:** Vanilla CSS (Professional Corporate Theme)
- **State Management:** React Context API (AuthContext)
- **Routing:** React Router DOM v6
- **HTTP Client:** Axios

## 📦 Setup & Installation

1.  **Prerequisites:** Node.js & npm

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    App will start at `http://localhost:5173`.

## 📂 Project Structure

```
src/
├── api/            # API client & endpoints
├── components/     # Reusable components (Navbar, Sidebar, etc.)
├── context/        # Global state (AuthContext)
├── pages/          # Page components (Login, Dashboard, Employees)
├── App.jsx         # Main routing & layout
└── index.css       # Global styles & variables
```

## 🔒 Route Permissions

| Path | Allowed Roles | Description |
| :--- | :--- | :--- |
| `/login` | Public | Login Page |
| `/dashboard` | All | Main Dashboard |
| `/employees` | All | Employee List |
| `/employees/add` | **Admin, HR** | Create New Employee |
| `/employees/edit/:id` | **Admin, HR** | Edit Employee |

## 🎨 Design System

The application uses a professional **Slate & Blue** color palette:
- **Primary:** `#0f172a` (Slate 900)
- **Accent:** `#3b82f6` (Blue 500)
- **Background:** `#f8fafc` (Slate 50)
