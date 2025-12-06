# 🍔 FastFood Delivery API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Prisma](https://img.shields.io/badge/Prisma-ORM-2D3748?style=for-the-badge&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-336791?style=for-the-badge&logo=postgresql)
![Security](https://img.shields.io/badge/Security-OAuth2_&_Bcrypt-red?style=for-the-badge&logo=security)

A scalable, asynchronous backend system for a generic food delivery
platform.\
Built with Python best practices, it features role-based access
control, dynamic menus, secure auth, and real-time order tracking.

------------------------------------------------------------------------

## 🚀 Key Features

-   **Asynchronous Backend**\
    Powered by `FastAPI`, `uvicorn`, and async Prisma client for high
    concurrency.

-   **Modern ORM**\
    Prisma Client Python ensures type-safe and expressive database
    interactions.

-   **Dynamic Menu System**\
    Admins can create, update, and manage categories like Burgers,
    Sushi, Drinks, etc.

-   **Order Management**

    -   Automatic total price calculation
    -   Lifecycle tracking
        (`PENDING → IN_TRANSIT → DELIVERED → CANCELLED`)
    -   Restricted visibility (users see only their orders; admins see
        everything)

-   **Strong Security**

    -   OAuth2 with JWT for stateless authentication\
    -   Password hashing using **Bcrypt**\
    -   Pydantic v2 validation for data integrity

------------------------------------------------------------------------

## 🛠 Tech Stack

-   **Framework:** FastAPI\
-   **Database:** PostgreSQL\
-   **ORM:** Prisma Python\
-   **Authentication:** OAuth2 + JWT (Python-Jose)\
-   **Password Hashing:** Bcrypt\
-   **Server:** Uvicorn (ASGI)\
-   **Configuration:** Pydantic Settings

------------------------------------------------------------------------

## 📂 Project Structure

    FOODDELIVERY/
    ├── app/
    │   ├── routers/
    │   │   ├── auth.py       # User Authentication (Signup/Login)
    │   │   ├── menu.py       # Admin Food Item Management
    │   │   └── orders.py     # Order Processing & Tracking
    │   ├── config.py         # Environment Configuration
    │   ├── database.py       # Prisma Client Instance
    │   ├── main.py           # App Entry Point
    │   ├── schemas.py        # Pydantic Models
    │   └── security.py       # Hashing & JWT Logic
    ├── prisma/
    │   └── schema.prisma     # Database Schema & Models
    ├── .env                  # Secrets (Ignored by Git)
    └── requirements.txt      # Dependencies

------------------------------------------------------------------------

## ⚡ Getting Started

### 1. Prerequisites

-   Python
-   PostgreSQL installed and running

------------------------------------------------------------------------

### 2. Installation

Clone the repository:

``` bash
git clone https://github.com/yourusername/food-delivery-backend.git
cd food-delivery-backend
```

Create a virtual environment

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 3. Environment Configuration

Create a `.env` file:

``` env
DATABASE_URL="postgresql://postgres:yourpassword@localhost:your_port/your_db_name?schema=public"

SECRET_KEY="change_this_to_a_secure_random_string"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=use_any
```

------------------------------------------------------------------------

### 4. Database Setup (Prisma)

``` bash
prisma generate
prisma db push
```

------------------------------------------------------------------------

### 5. Run the Server

``` bash
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## 📖 API Documentation

Swagger UI: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 🔗 Core Endpoints

### Auth

  Method   Endpoint         Access   Description
  -------- ---------------- -------- -----------------------
  POST     `/auth/signup`   Public   Register new user
  POST     `/auth/login`    Public   Login & receive token

### Menu

  Method   Endpoint       Access   Description
  -------- -------------- -------- -------------
  GET      `/menu/`       Public   List items
  POST     `/menu/`       Admin    Add item
  PUT      `/menu/{id}`   Admin    Update item

### Orders

  Method   Endpoint                Access   Description
  -------- ----------------------- -------- ---------------
  POST     `/orders/`              User     Place order
  GET      `/orders/me`            User     My orders
  GET      `/orders/`              Admin    All orders
  PUT      `/orders/status/{id}`   Admin    Update status

