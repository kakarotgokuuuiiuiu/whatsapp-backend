# whatsapp-backend

# WhatsApp Clone Backend

This is the backend API for the WhatsApp Clone project, built with Django REST Framework.

## Features

- REST API for managing users, messages, chats
- MongoDB database integration
- Message grouping by user
- Status tracking (sent, delivered, read)
- CORS configured for frontend integration

## Tech Stack

- Python 3.x
- Django 5.x
- Django REST Framework
- MongoDB (Atlas or local)
- Other dependencies as per requirements.txt

## Setup & Installation

1. Clone the repository
git clone https://github.com/your-username/your-backend-repo.gi
cd your-backend-repo

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

