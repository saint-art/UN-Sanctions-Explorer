# UN Security Council Sanctions Data Pipeline

## Project Overview

This project extracts, cleans, stores, and exposes data from the United Nations Security Council Consolidated Sanctions List.

The application demonstrates a complete data engineering pipeline, beginning with web scraping and ending with a searchable web application and REST API.

---

## Features

- Scrapes the official UN Security Council sanctions HTML dataset
- Cleans and normalizes extracted data
- Generates structured CSV datasets
- Imports data into a relational SQLite database
- Provides command-line search
- Provides a Flask web interface
- Provides REST API endpoints
- Displays dashboard statistics
- Displays complete sanction profiles including:
  - General information
  - Aliases
  - Passports
  - Addresses
  - Amendment history

---

## Technologies Used

- Python 3
- BeautifulSoup4
- Pandas
- SQLite
- Flask
- HTML
- CSS

---

## Database Schema

The project stores data in five relational tables.

- persons
- aliases
- passports
- addresses
- amendments

---

## Project Structure

```
UN_SANCTIONS/

app.py
api.py
database.py
sanctions_phase2.py
load_to_sqlite.py
search_sanctions.py

sanctions.db
schema.sql

templates/
static/
output/

README.md
requirements.txt
.gitignore
```

---

## Installation

Clone the repository.

Install dependencies.

```bash
pip install -r requirements.txt
```

Generate the CSV datasets.

```bash
python3 sanctions_phase2.py
```

Load the database.

```bash
python3 load_to_sqlite.py
```

Run the web application.

```bash
python3 app.py
```

Open your browser.

```
http://127.0.0.1:5000
```

---

## API Endpoints

### Search

```
GET /api/search?name=abbas
```

### Dashboard

```
GET /dashboard
```

### Health Check

```
GET /health
```

### Statistics

```
GET /stats
```

---

## Data Source

United Nations Security Council Consolidated Sanctions List

---

## Future Improvements

- MySQL database support
- SQLAlchemy ORM
- Authentication
- Pagination
- Advanced filtering
- Docker support
- Cloud deployment

---

## Author

Nelvin Mwendwa