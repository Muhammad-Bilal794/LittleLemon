# 🍋 LittleLemon Restaurant API

| Description | Screenshot |
|------------|------------|
| **LittleLemon** is a full-featured **Django REST API** designed for modern restaurant management — built as part of the **Meta Back-End Developer Capstone Project**.<br>It demonstrates **secure authentication**, **database management**, and **scalable RESTful API development** with **Django REST Framework** and **MySQL**. | <img src="https://i.postimg.cc/bvhMQzP8/Screenshot-2025-09-12-093917.png" width="400"/> |

---

## 🧠 Overview

The **LittleLemon API** is a backend system for managing restaurant operations, including:

- 🍽️ Menu Management (CRUD)
- 📅 Table Booking System (secure, token-protected)
- 🔑 Authentication via **JWT** and **DRF TokenAuth**
- 🧩 Modular structure with reusable serializers and views
- 🧪 Complete unit test coverage for endpoints and models

This project follows best practices for **clean architecture**, **API versioning**, and **secure backend design**.

---

## 🚀 Key Features

| Feature | Description |
|----------|-------------|
| 🧾 **Menu API** | Create, read, update, and delete menu items. |
| 🪑 **Booking API** | Manage customer table bookings with authentication. |
| 🔒 **Authentication** | Djoser integration for JWT & TokenAuth. |
| 🧠 **Permissions** | Access control with `IsAuthenticated`. |
| 🧰 **Admin Dashboard** | Manage all data using Django’s built-in admin. |
| 🧪 **Unit Testing** | Automated tests for views, serializers, and models. |
| 🗄️ **MySQL Database** | Fast, reliable, and production-grade data storage. |

---

## 🏗️ Tech Stack

- **Language:** Python 3  
- **Framework:** Django 5 & Django REST Framework  
- **Database:** MySQL  
- **Authentication:** Djoser (JWT + TokenAuth)  
- **Environment:** Virtualenv  
- **Testing:** Django TestCase framework  
- **API Client Tools:** Insomnia / Postman  

--- 


## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Muhammad-Bilal794/LittleLemon.git
cd LittleLemon
2️⃣ Create Virtual Environment
python -m venv env
env\Scripts\activate   # Windows
source env/bin/activate   # macOS/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Database

Edit LittleLemon/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LittleLemon',
        'USER': 'littlelemon_user',
        'PASSWORD': 'StrongPassword123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run Server
python manage.py runserver

Visit the app at:
👉 http://127.0.0.1:8000/restaurant/


🔗 API Endpoints
🍽️ Menu API
| Method    | Endpoint                 | Description            |
| --------- | ------------------------ | ---------------------- |
| GET       | `/restaurant/menu/`      | List all menu items    |
| POST      | `/restaurant/menu/`      | Create a new menu item |
| GET       | `/restaurant/menu/{id}/` | Retrieve a single item |
| PUT/PATCH | `/restaurant/menu/{id}/` | Update existing item   |
| DELETE    | `/restaurant/menu/{id}/` | Delete item            |

---
🪑 Booking API
| Method    | Endpoint                    | Description              |
| --------- | --------------------------- | ------------------------ |
| GET       | `/restaurant/booking/`      | View all bookings        |
| POST      | `/restaurant/booking/`      | Create a booking         |
| GET       | `/restaurant/booking/{id}/` | Retrieve booking details |
| PUT/PATCH | `/restaurant/booking/{id}/` | Update booking           |
| DELETE    | `/restaurant/booking/{id}/` | Delete booking           |

🔒 Authentication Endpoints
| Endpoint             | Description                  |
| -------------------- | ---------------------------- |
| `/auth/users/`       | Register a new user          |
| `/auth/jwt/create/`  | Login (obtain JWT token)     |
| `/auth/jwt/refresh/` | Refresh JWT token            |
| `/auth/jwt/verify/`  | Verify JWT token             |
| `/api-token-auth/`   | Obtain DRF token (TokenAuth) |

🧪 Running Tests
Run all unit tests using:

python manage.py test restaurant


✅ Tests include:

Model creation and field validation

Serializer behavior

View endpoint responses

Token-based authentication

```
## 🧠 Learning Outcomes

This project demonstrates:

- Secure API design using **Django REST Framework (DRF)** and **Djoser**
- Real-world authentication workflows (**JWT** & **TokenAuth**)
- Test-driven backend development
- API documentation and modular architecture

## 💼 Project Status

✅ **Completed Successfully**  
Built as part of the **Meta Back-End Developer Capstone Project** on Coursera.

## 🌍 Author

**Muhammad Bilal**  
📧 [mb3454545@gmail.com]  
🔗 [GitHub Profile](https://github.com/Muhammad-Bilal794)

## 🏷️ Repository Topics

`django` · `django-rest-framework` · `rest-api` · `backend-development` · `meta-backend` · `restaurant-management` · `mysql` · `jwt-authentication` · `token-authentication` · `api-security` · `djoser` · `python` · `fullstack` · `capstone-project`

## 🏁 Final Note

This project is a demonstration of **production-level backend development** using Django REST Framework — combining **security**, **scalability**, and **clean code architecture** for a real-world restaurant application. 🍋

## 🖼️ Screenshots

### Home Page
<img src="https://i.postimg.cc/bvhMQzP8/Screenshot-2025-09-12-093917.png" alt="Dashboard" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### Menu List
<img src="https://i.postimg.cc/BbjpDzwj/09-Er-Zt-U-TB6vqa-RVGq5-SYA-3cddf1ccbb30444fbeaca1aa6cc582e1-image.png" alt="User Profile" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### Token Creation
<img src="https://i.postimg.cc/28FGWn0d/SJk5-Aku-YSv6i-Vpe2-Li-X-TA-0e775179b589485d8a9262ecf765e9e1-image.png" alt="Menu List" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### Dynamic Content/Posts
<img src="https://i.postimg.cc/wT7xykx1/image.png" alt="Booking Page" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### Get , Posts requests for menu items
<img src="https://i.postimg.cc/ZRR27VMn/image.png" alt="Orders Page" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### put,patch,delete request for menu items
<img src="https://i.postimg.cc/tTsyZqpb/image.png" alt="Payment Page" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>

### 🔒 No Access Without Validation Token
<img src="https://i.postimg.cc/ZRp7D2xg/image.png" alt="Reports Page" style="width:400px; border:2px solid #ddd; border-radius:10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); margin-bottom:15px;"/>



 
