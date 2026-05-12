#  Django eCommerce Application

This project is a **Django-based eCommerce web application** that supports **vendors and buyers**, product management, shopping carts, checkout with email invoices, and product reviews.

This README provides **step-by-step instructions** to install, configure, and run the project to **full working order**.


##  Prerequisites

Before you begin, ensure you have the following installed on your system:

* Python **3.10+**
* pip (Python package manager)
* MariaDB or MySQL Server
* Git
* Virtual environment tool (optional but recommended)

Check versions:

```bash
python --version
pip --version

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce_project.git
cd ecommerce_project

## Step 2: Create & Activate Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate


##  Step 3: Install Dependencies

```bash
pip install -r requirements.txt


If `requirements.txt` does not exist yet:

```bash
pip install django mysqlclient
pip freeze > requirements.txt


##  Step 4: Configure the Database (MariaDB)

### Create Database

Login to MariaDB/MySQL:

```bash
mysql -u root -p


```sql
CREATE DATABASE ecommerce_db;
EXIT;


### Update `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


##  Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate


##  Step 6: Create Admin (Superuser)

```bash
python manage.py createsuperuser


Follow the prompts to create an admin account.


## Step 7: Configure Email (For Invoices & Password Reset)

Add this to `settings.py` (example using Gmail SMTP):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'

 Use an **App Password**, not your real email password.

##  Step 8: Run the Development Server

```bash
python manage.py runserver

Open your browser and go to:
http://127.0.0.1:8000/


##  Step 9: Using the Application

### Vendors

* Register as a vendor
* Create, edit, and delete stores
* Add, edit, and remove products

### Buyers

* Browse products from different stores
* Add products to cart
* Checkout and receive invoice via email
* Leave verified or unverified reviews

### Admin

* Access admin panel:

http://127.0.0.1:8000/admin/

## Step 10: Password Reset

1. Go to `/password-reset/`
2. Enter registered email address
3. Follow email link to reset password

✔ Token-based
✔ Secure
✔ Time-limited URL


##  Common Issues & Fixes

### mysqlclient install error

```bash
pip install mysqlclient

Ensure MariaDB/MySQL development headers are installed.

### Migration errors

```bash
python manage.py migrate --run-syncdb


## Features Implemented

* Vendor & Buyer roles
* Store & product management
* Session-based cart
* Checkout & email invoice
* Verified & unverified reviews
* Password recovery
* MariaDB integration


##  License

This project is for **educational purposes**.


## Author

Created as part of a Django eCommerce assignment.

