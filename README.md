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
├── requirements.txt
└── .gitignore
```

The SQLite database is generated locally during setup and is excluded from Git using `.gitignore`.

## Setup and Run

### 1. Open the project directory

Open a terminal in the `recruiter-bot-backend` project directory.

### 2. Create and activate a virtual environment

For Windows Command Prompt:

```cmd
py -m venv venv
venv\Scripts\activate.bat
```

If the virtual environment already exists, activate it using:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```cmd
python -m pip install -r requirements.txt
```

### 4. Create the database and seed the sample data

Create the database tables:

```cmd
python database.py
```

Insert the sample candidates, skills, jobs, and required skills:

```cmd
python seed_data.py
```

The seed script can be run repeatedly without creating duplicate candidate or job records.

### 5. Start the API

```cmd
python -m uvicorn main:app --reload
```

Open the interactive API documentation in your browser:

http://127.0.0.1:8000/docs

Keep the terminal running while using the API.

## API Endpoints

### 1. Candidates ranked for a job

**Endpoint:** `GET /jobs/{job_id}/matches`

Example:

```http
GET /jobs/1/matches
```

This endpoint returns candidates ranked by their match score for the specified job. Each result includes the candidate ID, name, availability, score, matched skills, skill score, experience score, and a short explanation.

Example using curl:

```bash
curl http://127.0.0.1:8000/jobs/1/matches
```

### 2. Jobs ranked for a candidate

**Endpoint:** `GET /candidates/{candidate_id}/matches`

Example:

```http
GET /candidates/1/matches
```

This endpoint returns jobs ranked by their match score for the specified candidate. Each result includes the job ID, title, tagline, score, matched skills, skill score, experience score, and a short explanation.

Example using curl:

```bash
curl http://127.0.0.1:8000/candidates/1/matches
```

### Error handling

Both endpoints return HTTP `404 Not Found` when the requested job or candidate ID does not exist.

## Matching Algorithm

The matching score combines two components:

- **Skill overlap:** 70% of the total score.
- **Experience fit:** 30% of the total score.

### Skill overlap

Skill overlap is calculated as the number of required skills possessed by a candidate divided by the total number of required skills.

`Skill Score = Matched Required Skills / Total Required Skills`

### Experience fit

Experience fit is calculated as the candidate's years of experience divided by the job's minimum experience, capped at 100%.

`Experience Score = min(Candidate Experience / Minimum Experience, 1)`

### Final score

`Match Score = (0.70 × Skill Score + 0.30 × Experience Score) × 100`

The scores are rounded to two decimal places.

### Ranking and explanations

Candidates are ranked in descending order of match score for a job. Jobs are ranked in descending order of match score for a candidate. Equal scores are resolved deterministically using candidate ID or job ID, respectively.

Each result includes a short explanation identifying the matched skills and whether the candidate meets the job's minimum experience requirement.

## Design Decisions and Trade-offs

### Database design

Candidates, jobs, candidate skills, and required job skills are stored in separate relational tables. This avoids storing multiple skills in a single comma-separated field and supports straightforward skill lookups and relationships.

### Scoring design

The matching algorithm uses a transparent, deterministic weighted score. Skill overlap receives the greater weight because required capabilities are central to a job match. Experience receives a smaller weight and is capped once the minimum experience requirement is met, preventing additional experience alone from dominating the ranking.

### Candidate eligibility

Candidates are not automatically excluded if they are marked as not looking for work or have less than the minimum experience. Availability and experience are included in the returned results and explanations rather than used as hard filters. This preserves a complete ranked list, although a production recruitment system could apply configurable eligibility rules.

### Technology choices

SQLite keeps the project lightweight and easy to run locally. FastAPI provides HTTP endpoints and interactive API documentation. SQL operations are written directly using Python's `sqlite3` module without an ORM or query builder.

### Limitations and possible improvements

For production use, the application could be extended with authentication, pagination, input validation, database migrations, logging, automated tests, and configurable matching weights. Availability and other candidate preferences could also be incorporated into the ranking or eligibility rules.

## SQL Detective Challenge

The five SQL Detective Challenge queries are provided separately in `sql_detective.sql`. They use the supplied `recruiters`, `job_postings`, `applicants`, and `interviews` schema.

The queries address:

1. Listing open job postings with recruiter information.
2. Counting applicants who reached the Final interview stage for each job posting.
3. Identifying people who appear to have applied to multiple jobs despite differences in email casing.
4. Calculating Final-stage interview conversion rates for recruiters with at least three Final-stage interviews.
5. Using a window function to identify the recruiter or recruiters with the most successful placements in each department.

For Question 3, email addresses are normalized using `LOWER()` and `TRIM()` to account for casing and surrounding whitespace. Because the supplied schema does not include a separate applications table, interview records are used as evidence of job-specific applicant activity. Consequently, this query identifies multiple job appearances evidenced by interview records rather than every application submitted.

For Question 5, a successful placement is defined as a Final-stage interview with an outcome of `passed`. The window function uses ranking so that ties for the highest number of successful placements are retained.

## AI Tool Disclosure

ChatGPT was used as a development assistant to help draft code, SQL queries, and documentation. The implementation and matching decisions should be reviewed and understood by the author before submission.