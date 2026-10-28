
# Recruiter Bot — Backend Developer Intern Assignment

## Overview

Recruiter Bot is a backend API that ranks candidates against jobs and jobs against candidates using skill overlap and experience fit. The project uses Python, FastAPI, SQLite, and handwritten SQL without an ORM or query builder.

## Technology Stack

- Python 3
- FastAPI
- Uvicorn
- SQLite
- Raw SQL

## Project Structure

```text
recruiter-bot-backend/
├── main.py
├── database.py
├── seed_data.py
├── matching.py
├── sql_detective.sql
├── README.md
├── recruiter_bot.db
└── venv/
```

## Setup and Run

Open a terminal in the project directory.

Create and activate a virtual environment on Windows:

```cmd
py -m venv venv
venv\Scripts\activate.bat
```

Install dependencies:

```cmd
python -m pip install fastapi uvicorn
```

Create the database tables and seed the sample data:

```cmd
python database.py
python seed_data.py
```

Start the API:

```cmd
python -m uvicorn main:app --reload
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## API Endpoints

### 1. Candidates ranked for a job

```http
GET /jobs/1/matches
```

Returns candidates ranked by their match score for the specified job, including matched skills and an explanation.

Example using curl:

```bash
curl http://127.0.0.1:8000/jobs/1/matches
```

### 2. Jobs ranked for a candidate

```http
GET /candidates/1/matches
```

Returns jobs ranked by their match score for the specified candidate, including matched skills and an explanation.

Example using curl:

```bash
curl http://127.0.0.1:8000/candidates/1/matches
```

Both endpoints return HTTP 404 when the requested job or candidate does not exist.

## Matching Algorithm

The matching score combines two components:

- Skill overlap: 70% of the total score.
- Experience fit: 30% of the total score.

Skill overlap is calculated as the number of required skills possessed by a candidate divided by the total number of required skills.

Experience fit is calculated as the candidate's years of experience divided by the job's minimum experience, capped at 100%.

The final score is:

`Match Score = (0.70 × Skill Score + 0.30 × Experience Score) × 100`

Candidates with the same score are ordered by candidate ID; jobs with the same score are ordered by job ID.

The reason returned for each match identifies the matched skills and whether the candidate meets the minimum experience requirement.

## Design Decisions and Trade-offs

Skills are stored in separate relational tables instead of comma-separated strings. This supports normalized data, straightforward skill lookups, and explicit relationships between candidates, jobs, and their skills.

The matching algorithm uses a transparent, deterministic weighted score. Skill overlap receives the greater weight because the required capabilities are central to a job match. Experience receives a smaller weight and is capped once the minimum requirement is met, preventing additional experience alone from dominating the ranking.

The current score does not automatically exclude candidates who are not looking for work or who have less than the minimum experience. Availability and minimum experience are reported in context rather than used as hard filters. This preserves a complete ranked list but could be changed according to product requirements.

SQLite keeps the project lightweight and easy to run locally. For a production system, additional work would be needed for authentication, pagination, data validation, migrations, logging, and a more comprehensive test suite.

## SQL Detective Challenge

The five SQL Detective Challenge queries are provided separately in `sql_detective.sql`. They use the supplied recruiters, job_postings, applicants, and interviews schema.

Question 3 uses interview records as evidence of applicants progressing through job-specific stages because the supplied schema does not include a separate applications table. Email casing and surrounding whitespace are normalized when grouping applicant records.

## AI Tool Disclosure

ChatGPT was used as a development assistant to help draft code, SQL queries, and documentation. The implementation and matching decisions should be reviewed and understood by the author before submission.
