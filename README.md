# NEURONA - Creator & Investor Platform

> Connecting visionary creators with investors through a secure, scalable, and intelligent innovation platform.

![Status](https://img.shields.io/badge/Status-🚧%20Under%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Preview
<p align="center">
  <img src="https://github.com/user-attachments/assets/0d867258-03b4-4205-8981-624a3d29d00d" width="900">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/363356a4-252f-43da-9cc6-12a48376a7ea" width="445">
  <img src="https://github.com/user-attachments/assets/87d8ba7c-240d-4409-9fc4-eb9d51e28ba2" width="445">
</p>

---

### 📖 OVERVIEW

Neurona is a modern full-stack platform designed to bridge the gap between **Creators** with innovative ideas and **Investors** seeking high-potential opportunities.

The platform enables creators to showcase projects, investors to discover and engage with innovative ideas, and administrators to efficiently manage the platform through dedicated dashboards.

Designed with scalability and maintainability in mind, Neurona follows a modular backend architecture powered by **FastAPI** and **PostgreSQL**.

> **Project Status:** 🚧 Active Development

---

### ✨ FEATURES

#### Authentication & Authorization
- Secure Registration & Login
- Password Hashing
- Session Authentication
- Role-Based Access Control
- Route Protection using Middleware

#### Creator Portal
- Creator Dashboard
- Project Submission
- Idea Management
- Profile Management
- Verification System

#### Investor Portal
- Investor Dashboard
- Browse Innovative Projects
- Express Investment Interest
- Profile Verification
- Saved Opportunities

#### Admin Portal
- User Management
- Creator Verification
- Investor Verification
- Platform Moderation
- Analytics Dashboard

#### Security
- Authentication Middleware
- Input Validation
- Error Handling
- Secure Password Storage
- Protected API Endpoints

---

### 🏛️ Backend Architecture

Neurona follows a layered architecture to keep the application scalable and maintainable.

```
Client
   │
   ▼
API Routes
   │
   ▼
Service Layer
   │
   ▼
Models / Schemas
   │
   ▼
PostgreSQL Database
```

Business logic is separated from API routes, allowing the application to remain modular and easy to extend.

---

### 🛠 TECH STACK

#### Backend
- FastAPI
- Python
- PostgreSQL

#### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

#### Development Tools
- Git
- GitHub
- VS Code

---

### 📂 Project Structure

```text
Neurona/
│
├── config/
│   └── settings.py
│
├── database/
│   └── database.py
│
├── middleware/
│   ├── auth_middleware.py
│   └── error_handlers.py
│
├── models/
│   ├── user.py
│   ├── creator_verification.py
│   └── investor_verification.py
│
├── routes/
│   ├── auth.py
│   ├── creator.py
│   ├── investor.py
│   ├── admin.py
│   └── index.py
│
├── schemas/
│   ├── user.py
│   ├── idea.py
│   └── investment.py
│
├── services/
│   ├── auth_service.py
│   ├── creator_service.py
│   ├── idea_service.py
|   └── investor_service.py
│
├── static/
|   ├── css/
|   ├── images/
|   ├── js/
|   └── uploads/investor_verification/
|
├── templates/
|   ├── admin/
|   ├── auth/
|   ├── creator/
|   ├── investor/
|   └── home/
|
├── utils/
│
├── main.py
├── requirements.txt
└── README.md
```

---

### Key Highlights

- Modular FastAPI Architecture
- Layered Backend Design
- Role-Based Authentication
- PostgreSQL Database
- Secure Verification System
- RESTful API Development
- Responsive Frontend
- Scalable Project Structure

---

### 🚧 Development Progress

| Module | Status |
|---------|--------|
| Authentication | ✅ Completed |
| Authorization | ✅ Completed |
| Creator Module | 🚧 In Progress |
| Investor Module | 🚧 In Progress |
| Admin Module | 🚧 In Progress |
| Verification System | 🚧 In Progress |
| PostgreSQL Integration | ✅ Completed |
| Deployment | ⏳ Planned |

---

### 🎯 Upcoming Features

- AI-powered Project Recommendation
- Intelligent Investor Matching
- Real-time Notifications
- Integrated Messaging
- Investment Tracking
- Payment Gateway Integration
- Email Verification
- Docker Support
- CI/CD Pipeline
- Cloud Deployment

---

### 🤝 Contributing

Contributions, suggestions, and feedback are welcome. Feel free to fork the repository, open issues, or submit pull requests.

---

### 📄 License

This project is licensed under the MIT License.

---

### 📄 Developer

**S.M. ABDULLAH TAWSIF**

- Computer Science & Engineering Student
- Aspiring Machine Learning Engineer
- Passionate about Backend Development, Artificial Intelligence, and Scalable Software Systems.

---

⭐ If you like this project, consider giving it a star!
