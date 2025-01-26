# CO2 Footprint Calculation API

## Overview
This project provides an API to calculate CO2 footprints, manage user authentication, and register new users. It includes three main endpoints:

- `emission/calc/` - Calculate CO2 footprint
- `users/login/` - Login for users
- `users/signup/` - Register new users

## Prerequisites

- Python 3.x
- Django

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/elsevar/code-green.git
   cd code-green
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Endpoints

### 1. Calculate CO2 Footprint (`users/calc/`)
- **Method**: POST
- **Description**: Calculates the CO2 footprint based on energy consumption and emission factors.

**Request Example**:
```json
[
  {
    "description": "Heating oil usage",
    "energy_source_id": "2001",
    "energy_consumption": "2500.0",
    "emission_factor": "0.28"
  },
  {
    "description": "Heating oil usage",
    "energy_source_id": "2001",
    "energy_consumption": "6000.0"
  }
]
```

**Response Example**:
```json
[
  {
    "name": "SCOPE_1",
    "label": "Brenn-/Treibstoffe, Kältemittel, Prozessemissionen",
    "energy": 93967.5,
    "co2": 26.58484,
    "children": [
      {
        "name": "1.1",
        "label": "Brennstoffe / Wärme",
        "energy": 93967.5,
        "co2": 26.58484,
        "children": [
          {
            "name": "1.1.1",
            "label": "Heizöl leicht (Heating oil usage)",
            "energy": 27637.5,
            "co2": 7.7385,
            "children": []
          },
          {
            "name": "1.1.2",
            "label": "Heizöl leicht (Heating oil usage)",
            "energy": 66330.0,
            "co2": 18.84634,
            "children": []
          }
        ]
      }
    ]
  }
]
```

### 2. Login (`users/login/`)
- **Method**: POST
- **Description**: Authenticate an existing user and obtain an access token.

**Request Example**:
```json
{
  "username": "username",
  "password": "password"
}
```

**Response Example**:
```json
{
  "message": "User authorized successfully.",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>"
}
```

### 3. Signup (`users/signup/`)
- **Method**: POST
- **Description**: Register a new user and obtain an access token.

**Request Example**:
```json
{
  "username": "username",
  "password": "password"
}
```

**Response Example**:
```json
{
  "message": "User created successfully.",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>"
}
```

## How to Use

1. **Register or Login**:
   - Use the `users/signup/` endpoint to create a new user.
   - Use the `users/login/` endpoint to log in and get an access token.

2. **Authorization**:
   - Add the access token to the request headers as a bearer token:
     ```
     Authorization: Bearer <access_token>
     ```

3. **Calculate CO2 Footprint**:
   - Send a POST request to the `users/calc/` endpoint with the required payload.

## Example Workflow
1. Register a new user:
   ```json
   POST /signup/
   {
     "username": "new_user",
     "password": "secure_password"
   }
   ```

2. Login to get tokens:
   ```json
   POST /login/
   {
     "username": "new_user",
     "password": "secure_password"
   }
   ```

3. Use the access token to calculate CO2 footprint:
   ```bash
   curl -X POST http://127.0.0.1:8000/emission/calc/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '[{...}]'
   ```
