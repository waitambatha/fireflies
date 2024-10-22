# Fireflies Transcript Sync

## Project Overview

The **Fireflies Transcript Sync** project is a Django-based application designed to sync meeting recording transcripts from Fireflies.ai via its RESTful API. This application allows users to authenticate, register, and retrieve meeting transcripts seamlessly. The application is built using Django REST Framework and incorporates features like JWT authentication, transcript management, and integration with Fireflies API.

## Features

- User registration and authentication with JWT.
- Sync meeting transcripts from Fireflies.
- View, create, update, and delete transcripts via a RESTful API.
- Custom error handling and response messages.
- Swagger documentation for easy API exploration.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JSON Web Tokens (JWT)
- **Database**: sqlite
- **Environment Variables**: `.env` file for sensitive configurations
- **API Client**: Integration with Fireflies API for fetching transcripts

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x or later
- sqlite
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/waitambatha/fireflies.git
   cd fireflies
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

bash
Copy code

Create a .env file in the root directory and add your Fireflies API key and database settings:

makefile
Copy code
BASE_URL=https://api.fireflies.ai/v1
API_KEY=your_fireflies_api_key


bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser (optional):

bash
Copy code
python manage.py createsuperuser
Running the Application
To start the Django development server, run:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/.

API Documentation
The API can be explored using Swagger documentation available at:

arduino
Copy code
http://127.0.0.1:8000/swagger/
Usage
Authentication
Register a new user: POST /api/register/
Login: POST /api/token/
Transcript Management
Get transcripts: GET /api/transcripts/
Create a transcript: POST /api/transcripts/
Update a transcript: PUT /api/transcripts/{id}/
Delete a transcript: DELETE /api/transcripts/{id}/
