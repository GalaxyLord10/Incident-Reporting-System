# Incident Reporting System

## Overview

The Incident Reporting System is a web-based application that provides a comprehensive solution for reporting, viewing, and managing incidents. Developed with Python's Flask framework, this application is built upon an MVC (Model-View-Controller) architecture. It offers a wide range of features like user authentication, role-based access, incident reporting, and administrative controls.

## Features

### User Authentication
- Secure login and session management.
- Registration for general users and administrators.
- Note: To register as an admin, you will have to go to /admin_register directly and sign up which will automatically make you into an administrator
- Validates form inputs and checks for existing email addresses.

### Dashboard
- User-specific dashboard based on role (Admin or General User).
- Admin dashboard provides an overview of total users and incidents.

### Incident Management
- Allows users to create, view, and update incidents.
- Administrators can manage all incidents, update their status, and view them based on user filters.

### User Management (Admin Only)
- View, edit, and delete users.
- Change user roles and account types.

### Logging
- Logs for user activities are maintained and can be viewed by administrators.

### Entities and Attributes:

1. **User**
    - `id` (Primary Key)
    - `email` (Unique, Not Null)
    - `password` (Not Null)
    - `role` (Default: "IncidentReportView")
    - `account_type` (Default: "general_user")
    
2. **Incident**
    - `id` (Primary Key)
    - `user_id` (Foreign Key, Not Null)
    - `system`
    - `product`
    - `issue`
    - `time_of_occurrence`
    - `status` (Default: "Ongoing")
    
3. **IncidentUpdate**
    - `id` (Primary Key)
    - `incident_id` (Foreign Key, Not Null)
    - `description`
    - `time` (Default: Current Timestamp)
    - `user_id` (Foreign Key, Not Null)

### Relationships:

1. A `User` can report multiple `Incidents`. Hence, one-to-many between `User` and `Incident`.
    - Foreign Key in `Incident`: `user_id`
  
2. An `Incident` can have multiple `IncidentUpdates`. Hence, one-to-many between `Incident` and `IncidentUpdate`.
    - Foreign Key in `IncidentUpdate`: `incident_id`

3. An `IncidentUpdate` is created by a `User`. Hence, one-to-many between `User` and `IncidentUpdate`.
    - Foreign Key in `IncidentUpdate`: `user_id`

Entity-Relationship-Diagram:

```
+---------------+      +---------------+      +------------------+
|     User      |      |   Incident    |      |  IncidentUpdate  |
+---------------+      +---------------+      +------------------+
| PK id         |<-----| FK user_id    |<-----| FK incident_id   |
| email         |      | PK id         |      | PK id            |
| password      |      | system        |      | description      |
| role          |      | product       |      | time             |
| account_type  |      | issue         |------| FK user_id        |
+---------------+      | time_of_occurrence |  +------------------+
                       | status             |
                       +--------------------+
```

In this ERD, "PK" denotes a Primary Key, "FK" denotes a Foreign Key, and the arrows indicate the direction of the relationships.

## Setup and Installation

### Prerequisites

- Python 3.x
- SQLite (Or you can configure another DBMS)
  
### Installation Steps

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the database setup script:
    ```bash
    python setup_db.py
    ```
5. Start the Flask application:
    ```bash
    python app.py
    ```

### Configuration

The configurations are located in `config.py`. For a production environment, it is advisable to set the `SECRET_KEY` and database credentials through environment variables.

## Dependencies

The application has several dependencies, including:

- Flask: For web development
- Flask-Login: For session management and user authentication
- SQLAlchemy: For database interaction
- Werkzeug: For password hashing
