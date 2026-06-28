# Python ETL Angular Project

## Overview

This project is a complete ETL pipeline application integrated with Neo4j graph database, FastAPI backend, and Angular frontend.

The project extracts football-related data from SQLite, transforms the data, loads it into Neo4j, and exposes APIs through FastAPI. The Angular frontend consumes these APIs and displays the data.

---

## Technologies Used

### Backend

- Python
- FastAPI
- Neo4j
- SQLite
- Pandas

### Frontend

- Angular
- TypeScript
- HTML/CSS

### Database

- Neo4j Graph Database
- SQLite

---

## Project Architecture

SQLite Database → ETL Pipeline → Neo4j → FastAPI APIs → Angular Frontend

---

## Features

- ETL pipeline implementation
- Neo4j graph database integration
- FastAPI REST APIs
- Angular frontend integration
- Team and player search APIs
- Authentication support
- Swagger API documentation

---

## Project Structure

```bash

PYTHON_ETL_PROJECT_MASTER/
│
├── Data/
│   ├── output/
│   ├── transformed/
│   └── database.sqlite
│
├── football-ui/
│   └── Angular frontend application
│
├── Phase 1/
│   ├── extractor.py
│   ├── config.yaml
│   ├── main.py
│   └── logs.txt
│
├── Phase 2/
│   ├── datamodel.py
│   ├── transformer.py
│   ├── loader.py
│   ├── utils.py
│   ├── config.yaml
│   ├── main.py
│   └── logs.txt
│
├── Phase 3/
│   ├── api_routes.py
│   ├── auth.py
│   ├── db_connector.py
│   ├── config.yaml
│   ├── main.py
│   └── logs.txt
│
├── common_utils.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Code-with-Shubham07/Python-ETL-Angular.git
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

#### Windows

```bash
venv\Scripts\activate
```

---

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt

```

---

## Neo4j Setup

Install Neo4j and create a local database instance.

Default Bolt URL:

```text
bolt://localhost:7687
```

Create `.env` file in project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

---

## Database File

Create `Data` folder in project root
Download `database.sqlite` from the link below and place it inside the `Data` folder.

Database Download Link:

https://drive.google.com/file/d/11q_rembfr3kHb4Rta6vU-xg5clgh96YE/view?usp=sharing

---

## Running Backend

### Phase 1 — Extraction

```bash
cd "Phase 1"
python main.py
```

### Phase 2 — Transform and Load into Neo4j

```bash
cd "../Phase 2"
python main.py
```

### Phase 3 — FastAPI Backend

```bash
cd "../Phase 3"
python main.py
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Authentication

Bearer token used:

```text
shubham
```

---

## Running Frontend

```bash
cd football-ui
npm install
npm start / ng serve
```

Frontend runs at:

```text
http://localhost:4200
```

---

## Future Improvements

- Docker support
- Deployment to cloud
- Advanced graph analytics
- Improved UI/UX
- Real-time updates

---

## Author

Shubham Kumar
