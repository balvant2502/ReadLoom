This is Ebook web application

## Setup Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your database credentials.
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

### Database Configuration
- This project uses PostgreSQL.
- Set your database details in a `.env` file (copy from `.env.example`).
- Do not commit `.env` to the repository.
