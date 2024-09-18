# Hospital Management System

This is a Django-based Hospital Management System API that manages appointments, user registrations, and roles (doctor, patient, etc.). The project includes custom user management, role-based views, appointment scheduling, and Swagger for Api documentation.

## Features

- **User Registration** with role-based fields
  - Doctors have a specialization field
  - Patients and other roles do not require specialization
- **Appointment Management**
  - Create, update, and filter appointments by doctor, patient, and status
- **Role-based Access Control**
  - Admins can create users
  - Doctors can manage appointments
- **API Endpoints** for managing users and appointments
- **Django Debug Toolbar** for easier debugging in development

## Requirements

- Python 3.x
- Django 4.x
- Django REST Framework
- Django Debug Toolbar

## Setup Instructions

### 1. Clone the repository

```bash
  git clone https://github.com/sadiqAjmal/Python_Week4_Assiginment.git
```
### 2. Install dependencies
Create a virtual environment and install the necessary dependencies:

bash
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure the database
Make sure to update your database settings in settings.py. By default, this project uses SQLite. You can also use PostgreSQL, MySQL, or any other database supported by Django.

### 4. Run migrations
```bash
python manage.py migrate
```
### 5. Create a superuser
Create an admin user to access the admin panel:

```bash
python manage.py createsuperuser
```
### 6. Start the development server
Run the server locally:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000 to access the application.

### API Endpoints
Here are some key API endpoints available in the project:

 - User Registration: users/register/<user_type>/
 - Register a new user, where <user_type> can be doctor, patient, etc.
 - Login: /users/auth/token
 - Swagger: /: This endpoint provides access to the Swagger UI, an interactive API documentation tool that allows developers to visualize and interact with the API's resources. Swagger simplifies testing by providing a web-based interface where you can execute API requests, view responses, and understand the structure of the available endpoints.

### Appointment Management:

List/Create Appointments: appointments/
Retrieve/Update/Delete Appointments: appointments/<id>/
Filter Appointments by doctor, date, or status

### Running Tests
To run the test suite:

```bash
python manage.py test api.users.tests.registerview_tests
python manage.py test api.users.tests.listview_tests
python manage.py test api.users.tests.detailview_tests
python manage.py test api.appointments.test
```
This project includes unit tests for user registration, role management, and appointment scheduling.

### Documentation
To view the api documentation run the project and view 127.0.0.1/redoc
