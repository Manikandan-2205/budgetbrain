# 💰 AI-Powered Personal Finance Tracker

A modern **personal finance management system** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **AI/ML** to help users automatically analyze, categorize, and forecast their spending habits.

---

## 🚀 Project Overview

This project helps users:
- Manage multiple bank accounts  
- Upload bank statements (PDF/CSV)  
- Automatically extract and categorize transactions using AI/ML  
- Visualize spending patterns and monthly budgets  
- Receive smart alerts for loan due dates, upcoming bills, and unusual transactions  

The backend is powered by **FastAPI** (Python 3.11+), using **PostgreSQL** for data persistence, **Redis** for caching, and **Machine Learning** for expense prediction and categorization.

---

## 🧩 Features

| Feature | Description |
|----------|--------------|
| 🔐 **JWT Auth System** | Secure login/signup with FastAPI & JWT tokens |
| 🧾 **Account Master** | Manage user bank accounts (account no, IFSC, bank name, type, etc.) |
| 📂 **Transaction Extractor** | Upload PDF or CSV bank statements → auto-parse using AI/ML |
| 📊 **Dashboard** | View categorized transactions, balance summaries, and trends |
| 🤖 **AI Financial Advisor** | ML model suggests saving patterns, detects anomalies |
| 🔔 **Smart Alerts** | Loan due date & low balance notifications |
| ⚙️ **Docker + PostgreSQL + Redis** | Fully containerized for local development |
| ☸️ **Kubernetes Ready** | Local Minikube deployment for scalability |

---

## 🧠 Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Alembic (DB migrations)
- PostgreSQL
- Redis (cache + background jobs)
- Pydantic
- Uvicorn (ASGI server)

**AI/ML:**
- scikit-learn / XGBoost (prediction)
- spaCy or Transformers (text extraction & classification)
- Pandas / NumPy (data processing)

**Frontend (optional next phase):**
- Flask / Streamlit / React Dashboard

**DevOps:**
- Docker & Docker Compose
- Minikube (Kubernetes)
- GitHub Actions (CI/CD)

---

## ⚙️ Project Setup (Local)

### 1️⃣ Clone Repository
```bash
