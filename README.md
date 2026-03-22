# Inventory Management System

A backend inventory system built with **Django** and **Django REST Framework (DRF)** for managing multi-warehouse business operations with secure role-based access and real-time stock tracking.

## Features

### Authentication & User Management
- Role-based authentication system (Admin, Manager, Sales)  
- Custom permissions for each user role  

### Product Management
- Add, edit, and delete products  
- QR code and barcode generation for each product  

### Stock Management
- Stock in/out system with editable transaction history  
- Multi-warehouse inventory tracking  

### Notifications
- Email notifications for product creation  
- Low stock alerts for admin users  

### Dashboard
- Daily stock insights  
- Reports of stock in/out  
- Low stock monitoring  

## Tech Stack
- **Backend:** Python, Django, Django REST Framework  
- **Database:** SQLite  
- **Authentication:** JWT  
- **Email:** SMTP  
- **Task Queue:** Celery & Redis  
- **Tools:** Git, Postman  

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/inventory-management.git
cd inventory-management
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
