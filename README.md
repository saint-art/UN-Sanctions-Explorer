# UN Security Council Sanctions Explorer

A modern Flask web application for searching and exploring the United 
Nations Security Council Consolidated Sanctions List.

---

## Features

- Fast full-text search
- Search by:
  - Full Name
  - Nationality
  - Sanction ID
- Individual profile pages
- Dashboard with database statistics
- API Documentation page
- Health monitoring page
- CSV Export
- Excel Export
- Responsive modern UI
- SQLite backend
- REST API

---

## Screenshots

Add screenshots here after deployment.

---

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

---

## Project Structure

```
UN-Sanctions-Explorer/

app.py
api.py
database.py
sanctions.db

templates/
static/

exports/

requirements.txt
README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/UN-Sanctions-Explorer.git
```

Move into the project

```bash
cd UN-Sanctions-Explorer
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python3 app.py
```

Open

```
http://127.0.0.1:5000
```

---

## Available Pages

| Route | Description |
|--------|-------------|
| / | Search Page |
| /dashboard | Dashboard |
| /docs | API Documentation |
| /health-ui | Health Monitor |
| /person/<id> | Person Profile |

---

## API Endpoints

### Health

```
GET /health
```

### Dashboard

```
GET /api/dashboard
```

---

## Database

SQLite relational database containing

- Persons
- Aliases
- Passports
- Addresses
- Amendments

---

## Future Improvements

- Docker support
- Authentication
- PostgreSQL support
- Dark mode
- Docker Compose
- CI/CD
- Cloud deployment

---

## Author

Nelvin Mwendwa

Python Backend Developer

Data Engineer
