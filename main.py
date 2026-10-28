
from fastapi import FastAPI, HTTPException

from database import initialize_database
from matching import get_matches_for_job, get_matches_for_candidate

app = FastAPI(
    title="Recruiter Bot API",
    description="Candidate and job matching API for Recruiterflow",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return {"message": "Recruiter Bot API is running"}


@app.get("/jobs/{job_id}/matches")
def job_matches(job_id: int):
    """Return candidates ranked by their match for a job."""
    matches = get_matches_for_job(job_id)

    if matches is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "matches": matches,
    }


@app.get("/candidates/{candidate_id}/matches")
def candidate_matches(candidate_id: int):
    """Return jobs ranked by their match for a candidate."""
    matches = get_matches_for_candidate(candidate_id)

    if matches is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {
        "candidate_id": candidate_id,
        "matches": matches,
    }
