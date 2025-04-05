# 🛠️ Document Categorization Backend

This is the Django REST Framework-based backend of the Document Categorization system. It supports user authentication, document upload, automatic text extraction, and intelligent categorization using keyword matching.

---

## 🚀 Features

- ✅ JWT-based Authentication
- 📄 File Upload (PDF, JPG, PNG)
- 🔍 OCR-based Text Extraction
- 🧠 Auto Categorization (Tax, Identity, Medical, Real Estate)
- 🔁 Category Update via API
- 🔐 Protected Routes

---

## ⚙️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- Tesseract OCR
- PostgreSQL / SQLite (local)
- JWT Authentication (SimpleJWT)

---

## 📦 Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   
 2. **Install dependencies**  
     ```bash
     pip install -r requirements.txt
 3. **Run migrations**  
     ```bash
     python manage.py migrate

 4. **Run server**  
     ```bash
     python manage.py runserver
 5. **You can create a user manually**  
     ```bash
     python manage.py createsuperuser

 
