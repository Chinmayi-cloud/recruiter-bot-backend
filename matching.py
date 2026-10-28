from database import get_connection


SKILL_WEIGHT = 0.70
EXPERIENCE_WEIGHT = 0.30


def calculate_match(candidate, candidate_skills, job, required_skills):
    """Calculate a match score and explanation for one candidate-job pair."""

    candidate_skill_set = set(candidate_skills)
    required_skill_set = set(required_skills)

    if required_skill_set:
        matched_skills = candidate_skill_set & required_skill_set
        skill_score = len(matched_skills) / len(required_skill_set)
    else:
        matched_skills = set()
        skill_score = 1.0

    minimum_experience = job["minimum_experience"]
    candidate_experience = candidate["experience_years"]

    if minimum_experience <= 0:
        experience_score = 1.0
    else:
        experience_score = min(candidate_experience / minimum_experience, 1.0)

    score = (
        SKILL_WEIGHT * skill_score
        + EXPERIENCE_WEIGHT * experience_score
    ) * 100

    if matched_skills:
        skill_reason = (
            "Matched skills: " + ", ".join(sorted(matched_skills))
        )
    else:
        skill_reason = "No required skills matched"

    if candidate_experience >= minimum_experience:
        experience_reason = (
            f"{candidate_experience} years of experience meets "
            f"the {minimum_experience}-year minimum"
        )
    else:
        experience_reason = (
            f"{candidate_experience} years of experience is below "
            f"the {minimum_experience}-year minimum"
        )

    reason = f"{skill_reason}. {experience_reason}."

    return {
        "score": round(score, 2),
        "reason": reason,
        "matched_skills": sorted(matched_skills),
        "skill_score": round(skill_score * 100, 2),
        "experience_score": round(experience_score * 100, 2),
    }


def get_candidate_skills(cursor, candidate_id):
    cursor.execute("""
        SELECT skill
        FROM candidate_skills
        WHERE candidate_id = ?
        ORDER BY skill
    """, (candidate_id,))
    return [row["skill"] for row in cursor.fetchall()]


def get_job_required_skills(cursor, job_id):
    cursor.execute("""
        SELECT skill
        FROM job_required_skills
        WHERE job_id = ?
        ORDER BY skill
    """, (job_id,))
    return [row["skill"] for row in cursor.fetchall()]


def get_matches_for_job(job_id):
    """Rank all candidates for a particular job."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    if job is None:
        connection.close()
        return None

    required_skills = get_job_required_skills(cursor, job_id)

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    results = []

    for candidate in candidates:
        skills = get_candidate_skills(cursor, candidate["id"])
        match = calculate_match(
            candidate, skills, job, required_skills
        )

        results.append({
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "availability": candidate["availability"],
            **match,
        })

    connection.close()

    results.sort(
        key=lambda item: (-item["score"], item["candidate_id"])
    )
    return results


def get_matches_for_candidate(candidate_id):
    """Rank all jobs for a particular candidate."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM candidates WHERE id = ?",
        (candidate_id,)
    )
    candidate = cursor.fetchone()

    if candidate is None:
        connection.close()
        return None

    candidate_skills = get_candidate_skills(cursor, candidate_id)

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    results = []

    for job in jobs:
        required_skills = get_job_required_skills(cursor, job["id"])
        match = calculate_match(
            candidate, candidate_skills, job, required_skills
        )

        results.append({
            "job_id": job["id"],
            "job_title": job["title"],
            "tagline": job["tagline"],
            **match,
        })

    connection.close()

    results.sort(
        key=lambda item: (-item["score"], item["job_id"])
    )
    return results