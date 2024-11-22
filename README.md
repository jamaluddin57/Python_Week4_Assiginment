# HealthSync - Comprehensive Care Coordination System

HealthSync is a robust Django backend system designed to manage hospital operations efficiently. It centralizes the management of users, appointments, and medical records, providing tailored access for various roles to ensure smooth operations across all levels of the organization. From booking appointments to maintaining comprehensive patient histories, HealthSync empowers healthcare facilities to operate with precision and ease.

## Core Capabilities

- **Streamlined Role Management:**
  - Tailored role-based access for administrators, medical professionals, and patients.
  - Administrators manage user accounts and system integrity.
  - Medical professionals access relevant appointments and medical histories.

- **Dynamic Appointment System:**
  - Flexible scheduling options for patient visits.
  - Ability to update or cancel appointments.
  - Appointments can be filtered by healthcare provider, date, or status.

- **Integrated Medical Records:**
  - Comprehensive patient histories including diagnostic data and treatment plans.
  - Quick search and retrieval of patient details.

- **Doctor Specialization Management:**
  - Track and manage doctor specializations.
  - Easy role and specialization updates by administrators.

- **Interactive API for Developers:**
  - Full API integration with Swagger and Redoc documentation.
  - Extensible for connection with telemedicine platforms or external databases.

- **Optimized Debugging and Testing Tools:**
  - Includes Django Debug Toolbar for real-time error tracing.
  - Extensive unit testing environment for stable deployment.


## Requirements

- Python 3.10+
- Django 5.1
- Django REST Framework
- Django Debug Toolbar

## Setup Instructions

### 1. Clone the repository

```bash
  git clone https://github.com/jamaluddin57/Python_Week4_Assiginment.git
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


### Documentation
To view the api documentation run the project and view 127.0.0.1/redoc
