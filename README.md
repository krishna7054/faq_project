# Multilingual FAQ Management System

## Overview

This project is a **Multilingual FAQ Management System** built using Django. It supports **rich text formatting** with `django-ckeditor`, **multilingual translations** using `googletrans`, and **caching** with `Redis` for optimized performance.

## Features

- **Rich Text Editor** for FAQ answers using `django-ckeditor`
- **Automatic Translation** of questions and answers using `googletrans`
- **Language-Specific API Filtering** (e.g., `?lang=hi` for Hindi FAQs)
- **Caching with Redis** for improved response times
- **REST API for Managing FAQs**
- **Admin Panel** for easy FAQ management

## Installation Steps

### 1️⃣ Clone the Repository

```bash
 git clone https://github.com/krishna7054/faq_project.git
 cd faq_project
```
### 2️⃣ Create & Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Redis (For Caching)

Make sure Redis is installed and running:

```bash
redis-server
```

If Redis is not installed, you can run it using Docker:

```bash
docker run --name redis-server -p 6379:6379 -d redis
```

### 5️⃣ Run Migrations & Start the Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create an admin user
python manage.py runserver
```

### 6️⃣ Access the Application

- **Django Admin Panel:** `http://127.0.0.1:8000/admin/`
- **API Endpoint:** `http://127.0.0.1:8000/api/faqs/`

## API Usage Examples

### 🔹 Fetch All FAQs in English (Default)

```bash
curl http://127.0.0.1:8000/api/faqs/
```

### 🔹 Fetch FAQs in Hindi

```bash
curl http://127.0.0.1:8000/api/faqs/?lang=hi
```

### 🔹 Fetch FAQs in Bengali

```bash
curl http://127.0.0.1:8000/api/faqs/?lang=bn
```

### 🔹 Create a New FAQ (Using cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/faqs/ -H "Content-Type: application/json" \
-d '{
    "question": "What is Django?",
    "answer": "Django is a high-level Python web framework."
}'
```

### 🔹 Update an FAQ

```bash
curl -X PUT http://127.0.0.1:8000/api/faqs/1/ -H "Content-Type: application/json" \
-d '{
    "question": "What is Django?",
    "answer": "Django is an open-source Python web framework."
}'
```

### 🔹 Delete an FAQ

```bash
curl -X DELETE http://127.0.0.1:8000/api/faqs/1/
```

## Docker Support

- Add a `Dockerfile` and `docker-compose.yml` for containerized deployment

### Build and run with Docker:
```bash
docker-compose up --build  
```

