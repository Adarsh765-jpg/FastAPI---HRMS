# Learning & Development Log
## Period: November 17 - December 5, 2024

---

## **Week 1: Foundation & Learning Phase**

### **Day 1 - November 17, 2024 (Sunday)**

**My Space:**
Started my journey into full-stack development by researching modern web technologies. Focused on understanding the fundamentals of REST APIs and why FastAPI is gaining popularity over Flask for building modern APIs.

**Tasks Carried Out:**
- Researched FastAPI framework and its advantages (async support, automatic documentation, type hints)
- Studied React fundamentals: components, props, state, and hooks
- Explored JWT authentication concepts and token-based security
- Set up development environment (Python 3.10+, Node.js, VS Code)

**Key Learnings:**
- FastAPI uses Python type hints for automatic validation and documentation
- React's component-based architecture promotes reusability
- JWT tokens consist of three parts: header, payload, and signature
- Understanding the difference between authentication (who you are) and authorization (what you can do)

**Tools, Equipment & Techniques:**
- VS Code with Python and JavaScript extensions
- Python 3.10, pip package manager
- Node.js v18+, npm
- Git for version control
- Postman for API testing (installed)

---

### **Day 2 - November 18, 2024 (Monday)**

**My Space:**
Dove deeper into FastAPI by following official documentation and building simple practice endpoints. Started understanding Pydantic models for data validation.

**Tasks Carried Out:**
- Created first FastAPI "Hello World" application
- Practiced creating GET, POST, PUT, DELETE endpoints
- Learned about Pydantic BaseModel for request/response validation
- Experimented with FastAPI's automatic Swagger UI documentation
- Studied SQLModel as an ORM combining SQLAlchemy and Pydantic

**Key Learnings:**
- FastAPI automatically generates OpenAPI documentation at `/docs`
- Pydantic validates data at runtime and provides clear error messages
- Type hints in Python aren't just for documentation - they enable powerful features
- SQLModel simplifies database operations by combining ORM with validation

**Tools, Equipment & Techniques:**
- FastAPI framework
- Pydantic for data validation
- Uvicorn ASGI server
- SQLModel for database operations
- Interactive API documentation (Swagger UI)

---

### **Day 3 - November 19, 2024 (Tuesday)**

**My Space:**
Focused on React fundamentals by building small practice components. Learned about React Router for navigation and how to manage application state.

**Tasks Carried Out:**
- Created practice React app using Vite (faster than Create React App)
- Built reusable components: Button, Card, Form inputs
- Practiced useState and useEffect hooks
- Implemented basic routing with React Router DOM v6
- Learned about props drilling and why context API is useful

**Key Learnings:**
- Vite provides significantly faster development experience than CRA
- React hooks allow functional components to have state and lifecycle methods
- useEffect dependencies array controls when side effects run
- React Router v6 uses different syntax than v5 (Routes instead of Switch)

**Tools, Equipment & Techniques:**
- Vite build tool
- React 19
- React Router DOM v7
- Chrome DevTools React extension
- Component composition patterns

---

### **Day 4 - November 20, 2024 (Wednesday)**

**My Space:**
Studied authentication and authorization patterns. Learned how to implement JWT-based auth in FastAPI and how to store tokens securely in the frontend.

**Tasks Carried Out:**
- Researched bcrypt for password hashing
- Implemented simple login endpoint with JWT token generation
- Learned about PyJWT library for encoding/decoding tokens
- Studied localStorage vs sessionStorage for token storage
- Created practice AuthContext in React for global auth state

**Key Learnings:**
- Never store passwords in plain text - always hash with bcrypt
- JWT tokens should have expiration times for security
- localStorage persists across browser sessions, sessionStorage doesn't
- Context API prevents prop drilling for global state like authentication
- Token should be sent in Authorization header as "Bearer <token>"

**Tools, Equipment & Techniques:**
- PyJWT library
- Passlib with bcrypt for password hashing
- React Context API
- Axios for HTTP requests
- JWT.io for debugging tokens

---

### **Day 5 - November 21, 2024 (Thursday)**

**My Space:**
Learned about Role-Based Access Control (RBAC) and how to implement it properly. Understood the importance of checking permissions on both frontend and backend.

**Tasks Carried Out:**
- Studied RBAC concepts: roles, permissions, and access control
- Created practice middleware for role checking in FastAPI
- Implemented protected routes in React
- Learned about dependency injection in FastAPI
- Practiced creating custom hooks in React

**Key Learnings:**
- RBAC should be enforced on the backend - frontend checks are just for UX
- FastAPI's Depends() enables clean dependency injection
- Custom React hooks can encapsulate reusable logic
- Protected routes should redirect unauthorized users to login
- Role hierarchy: Admin > HR > Employee

**Tools, Equipment & Techniques:**
- FastAPI dependencies system
- Custom React hooks
- React Router's Navigate component
- Middleware pattern for authentication
- Decorator pattern for route protection

---

### **Day 6 - November 22, 2024 (Friday)**

**My Space:**
Practiced database design and relationships. Created practice CRUD operations with SQLModel and learned about database migrations.

**Tasks Carried Out:**
- Designed employee database schema with relationships
- Practiced SQLModel table definitions with relationships
- Implemented basic CRUD operations for practice
- Learned about database sessions and connection management
- Studied pagination and filtering techniques

**Key Learnings:**
- Database relationships: One-to-One (User-Employee), One-to-Many
- SQLModel's relationship() function handles foreign keys elegantly
- Always use database sessions properly (open, use, close)
- Pagination improves performance for large datasets
- Filtering and searching should use database queries, not Python loops

**Tools, Equipment & Techniques:**
- SQLite for development database
- SQLModel ORM
- DB Browser for SQLite (for viewing database)
- Query optimization techniques
- Database session management patterns

---

### **Day 7 - November 23, 2024 (Saturday)**

**My Space:**
Consolidated learning by building a mini practice project combining all concepts. Created a simple task management API with React frontend.

**Tasks Carried Out:**
- Built practice CRUD API with authentication
- Created React frontend with login and protected routes
- Implemented role-based UI rendering
- Practiced error handling on both frontend and backend
- Tested API endpoints with Postman

**Key Learnings:**
- Integration is where you discover gaps in understanding
- Error handling is crucial for good user experience
- CORS configuration is necessary for frontend-backend communication
- Consistent API response format makes frontend easier
- Testing as you build prevents bugs from accumulating

**Tools, Equipment & Techniques:**
- Full-stack integration
- Postman for API testing
- CORS configuration
- Error handling patterns
- Try-catch blocks and error boundaries

---

## **Week 2: Project Planning & Initial Setup**

### **Day 8 - November 24, 2024 (Sunday)**

**My Space:**
Started planning the HRMS project. Defined requirements, created database schema, and planned the API endpoints and frontend pages.

**Tasks Carried Out:**
- Defined project requirements and features
- Designed database schema (User, Employee tables with relationships)
- Planned API endpoints structure
- Created wireframes for frontend pages
- Set up project folder structure (backend/ and frontend/)
- Initialized Git repository

**Key Learnings:**
- Planning before coding saves time and prevents rework
- Clear separation of concerns: models, schemas, routers, services
- Frontend structure: pages, components, context, api
- Version control from day one is essential

**Tools, Equipment & Techniques:**
- Git for version control
- Folder structure best practices
- Database schema design
- API endpoint planning
- Wireframing (pen and paper)

---

### **Day 9 - November 25, 2024 (Monday)**

**My Space:**
Set up the backend foundation. Created project structure, configured database, and implemented core configuration files.

**Tasks Carried Out:**
- Created backend folder structure (app/models, routers, schemas, services, utils)
- Set up config.py with environment variables
- Implemented database.py with SQLModel engine and session
- Created .env.example file for configuration template
- Set up requirements.txt with all dependencies
- Initialized SQLite database

**Key Learnings:**
- Environment variables keep sensitive data out of code
- Pydantic Settings makes config management elegant
- Separating database logic from business logic improves maintainability
- requirements.txt ensures reproducible environments

**Tools, Equipment & Techniques:**
- Pydantic Settings for configuration
- SQLModel for database setup
- Environment variables (.env file)
- Python package management
- Modular project structure

---

### **Day 10 - November 26, 2024 (Tuesday)**

**My Space:**
Built the core models and schemas for the application. Implemented User and Employee models with proper relationships.

**Tasks Carried Out:**
- Created user_model.py with User table (id, email, password, role)
- Created employee_model.py with Employee table (personal info, department, salary)
- Defined relationship between User and Employee (One-to-One)
- Created Pydantic schemas for request/response validation
- Implemented password hashing utility in utils/hashing.py

**Key Learnings:**
- SQLModel Field() allows setting constraints (unique, index, nullable)
- Relationship() with back_populates creates bidirectional relationships
- Separate schemas for Create, Update, and Response prevents data leaks
- Never return password hashes in API responses

**Tools, Equipment & Techniques:**
- SQLModel Field and Relationship
- Pydantic BaseModel for schemas
- Passlib bcrypt for password hashing
- Type hints for better code quality
- Optional fields for partial updates

---

### **Day 11 - November 27, 2024 (Wednesday)**

**My Space:**
Implemented authentication system with JWT tokens. Created login endpoint and auth dependencies for protected routes.

**Tasks Carried Out:**
- Created jwt_service.py for token creation and verification
- Implemented auth_router.py with /login endpoint
- Created auth.py dependency for extracting current user from token
- Added role checking utilities in utils/role_check.py
- Tested authentication flow with Postman

**Key Learnings:**
- JWT payload should include user ID and role for authorization
- Token expiration (24 hours) balances security and UX
- FastAPI's Depends() makes auth checking clean and reusable
- HTTPException with proper status codes improves API clarity

**Tools, Equipment & Techniques:**
- PyJWT for token operations
- FastAPI HTTPException
- Dependency injection pattern
- Bearer token authentication
- Postman for auth testing

---

### **Day 12 - November 28, 2024 (Thursday)**

**My Space:**
Built the employee service layer and router with full CRUD operations and RBAC enforcement.

**Tasks Carried Out:**
- Created employee_service.py with business logic
- Implemented employee_router.py with all CRUD endpoints
- Added RBAC checks: Admin (full access), HR (limited), Employee (read-only)
- Implemented pagination, filtering, and search functionality
- Created seed_data.py for default users (admin, hr, employee)

**Key Learnings:**
- Service layer separates business logic from route handlers
- RBAC must be enforced at every endpoint, not just frontend
- HR can create employees but not admins or other HR users
- Employees can only view their own data, not others
- Pagination parameters: skip and limit

**Tools, Equipment & Techniques:**
- Service layer pattern
- RBAC enforcement
- Query filtering with SQLModel
- Database seeding
- RESTful API design

---

### **Day 13 - November 29, 2024 (Friday)**

**My Space:**
Completed backend by adding main.py, CORS configuration, and comprehensive testing. Backend is now fully functional.

**Tasks Carried Out:**
- Created main.py with FastAPI app initialization
- Configured CORS for frontend communication
- Added startup event to create tables and seed data
- Created test_comprehensive.py with pytest
- Tested all endpoints and RBAC rules
- Created start.bat for easy server startup

**Key Learnings:**
- CORS must allow frontend origin for development
- Startup events are perfect for database initialization
- Comprehensive testing catches RBAC violations
- pytest with httpx makes API testing straightforward

**Tools, Equipment & Techniques:**
- FastAPI CORS middleware
- Pytest for testing
- httpx for test client
- Batch scripts for automation
- Swagger UI for manual testing

---

## **Week 3: Frontend Development**

### **Day 14 - November 30, 2024 (Saturday)**

**My Space:**
Started frontend development. Set up React project with Vite, configured routing, and created the authentication context.

**Tasks Carried Out:**
- Initialized React project with Vite
- Installed dependencies (react-router-dom, axios)
- Created AuthContext for global authentication state
- Set up React Router with route definitions
- Created .env file for API base URL
- Implemented ProtectedRoute component

**Key Learnings:**
- Vite's dev server is incredibly fast
- AuthContext provides login, logout, and user state globally
- ProtectedRoute checks auth before rendering protected pages
- Environment variables in Vite use VITE_ prefix

**Tools, Equipment & Techniques:**
- Vite build tool
- React Context API
- React Router DOM v7
- Axios HTTP client
- Environment variables

---

### **Day 15 - December 1, 2024 (Sunday)**

**My Space:**
Built the authentication flow and API client. Created login page and axios configuration with interceptors.

**Tasks Carried Out:**
- Created axiosClient.js with base URL and interceptors
- Implemented automatic token attachment to requests
- Built Login.jsx page with form and error handling
- Created Login.css with professional styling
- Implemented employeeAPI.js with all API methods
- Tested login flow with backend

**Key Learnings:**
- Axios interceptors automatically add auth headers to all requests
- localStorage.getItem() retrieves token for API calls
- Form validation improves user experience
- Error messages should be user-friendly, not technical

**Tools, Equipment & Techniques:**
- Axios interceptors
- localStorage API
- Form handling in React
- CSS styling techniques
- Error handling patterns

---

### **Day 16 - December 2, 2024 (Monday)**

**My Space:**
Created the main layout components: Navbar, Sidebar, and Layout wrapper. Implemented role-based UI rendering.

**Tasks Carried Out:**
- Built Navbar.jsx with user info and logout button
- Created Sidebar.jsx with navigation links
- Implemented Layout.jsx combining Navbar and Sidebar
- Added role-based menu item visibility
- Styled components with professional corporate theme
- Used CSS variables for consistent theming

**Key Learnings:**
- Layout component wraps all protected pages
- Sidebar navigation should reflect user's role permissions
- CSS variables (--primary-color) enable easy theming
- Flexbox is perfect for navbar and sidebar layouts

**Tools, Equipment & Techniques:**
- React component composition
- CSS Flexbox layout
- CSS custom properties (variables)
- Conditional rendering based on role
- Professional color palette (Slate & Blue)

---

### **Day 17 - December 3, 2024 (Tuesday)**

**My Space:**
Built the core pages: Dashboard and Employee List. Implemented pagination, search, and filtering functionality.

**Tasks Carried Out:**
- Created Dashboard.jsx with welcome message and stats cards
- Built Employees.jsx with table view and pagination
- Implemented search by name functionality
- Added filter dropdowns for department and role
- Created responsive table design
- Added loading states and error handling

**Key Learnings:**
- Dashboard provides quick overview of system
- Pagination prevents performance issues with large datasets
- Debouncing search input improves performance
- Filter combinations should work together (AND logic)
- Loading states improve perceived performance

**Tools, Equipment & Techniques:**
- React useState for local state
- useEffect for data fetching
- Array filter and map methods
- CSS Grid for stats cards
- Responsive table design

---

### **Day 18 - December 4, 2024 (Wednesday)**

**My Space:**
Completed the employee management features. Built Add/Edit forms with role-based restrictions and validation.

**Tasks Carried Out:**
- Created EmployeeForm.jsx for both add and edit modes
- Implemented form validation (required fields, email format)
- Added role-based restrictions (HR can only create Employees)
- Built EmployeeDetail.jsx for viewing single employee
- Implemented delete functionality with confirmation
- Added success/error notifications

**Key Learnings:**
- Single form component can handle both create and update
- useParams() hook gets route parameters (employee ID)
- Form validation should happen before API call
- Confirmation dialogs prevent accidental deletions
- HR users see disabled role dropdown locked to "Employee"

**Tools, Equipment & Techniques:**
- React Router useParams and useNavigate
- Form validation techniques
- Conditional form fields based on role
- Window.confirm() for delete confirmation
- RESTful API integration

---

### **Day 19 - December 5, 2024 (Thursday)**

**My Space:**
Final day - polished the application, added finishing touches, and created comprehensive documentation.

**Tasks Carried Out:**
- Refined CSS styling for consistency across all pages
- Added hover effects and transitions for better UX
- Created README.md files for both frontend and backend
- Wrote deployment_guide.md with production instructions
- Tested entire application flow for all three roles
- Fixed minor bugs and edge cases
- Created .env.example files for easy setup

**Key Learnings:**
- Small UI details (hover effects, transitions) make big difference
- Documentation is crucial for project handoff and future maintenance
- Testing with all user roles reveals hidden bugs
- Example environment files help others set up the project
- Deployment guide should cover security considerations

**Tools, Equipment & Techniques:**
- CSS transitions and hover effects
- Markdown documentation
- End-to-end testing
- Security best practices
- Production deployment considerations

---

## **Summary**

**Total Duration:** 19 days (November 17 - December 5, 2024)

**Project Outcome:** 
Fully functional HRMS (Human Resource Management System) with:
- FastAPI backend with JWT authentication and RBAC
- React frontend with role-based UI
- Complete CRUD operations for employee management
- Three user roles: Admin, HR, Employee
- Professional corporate design
- Comprehensive documentation

**Technologies Mastered:**
- Backend: FastAPI, SQLModel, PyJWT, Passlib, Pydantic
- Frontend: React, Vite, React Router, Axios, Context API
- Database: SQLite with potential PostgreSQL migration
- Tools: Git, Postman, pytest, VS Code

**Key Achievement:**
Successfully transitioned from learning fundamentals to building a production-ready full-stack application with proper architecture, security, and user experience considerations.

