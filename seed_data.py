import sqlite3
from database import get_connection, initialize_database


CANDIDATES = [
    {
        "name": "Sherlock H.",
        "skills": ["deduction", "pattern-recognition", "forensics"],
        "experience": 8,
        "availability": "Immediate",
        "traits": "analytical, blunt",
        "quirk": "Solves problems by eliminating the impossible; insufferable in standups."
    },
    {
        "name": "Hermione G.",
        "skills": ["research", "time-management", "public-speaking"],
        "experience": 4,
        "availability": "2 weeks",
        "traits": "detail-oriented, overachiever",
        "quirk": "Reads full documentation before coding."
    },
    {
        "name": "Tony S.",
        "skills": ["systems-design", "rapid-prototyping", "leadership"],
        "experience": 12,
        "availability": "Not looking",
        "traits": "confident, innovative",
        "quirk": "Ships an MVP overnight but refuses to write tests."
    },
    {
        "name": "Leslie K.",
        "skills": ["project-management", "stakeholder-management", "public-speaking"],
        "experience": 6,
        "availability": "Immediate",
        "traits": "tenacious, organized",
        "quirk": "Has a binder for everything."
    },
    {
        "name": "Ron S.",
        "skills": ["woodworking", "minimalism", "negotiation"],
        "experience": 15,
        "availability": "Not looking",
        "traits": "stubborn, principled",
        "quirk": "Refuses to use more than one monitor."
    },
    {
        "name": "Rick S.",
        "skills": ["systems-design", "rapid-prototyping", "chemistry"],
        "experience": 20,
        "availability": "Immediate",
        "traits": "genius, reckless",
        "quirk": "The solution works, but the mechanism is concerning."
    },
    {
        "name": "Elle W.",
        "skills": ["persuasion", "research", "public-speaking"],
        "experience": 3,
        "availability": "Immediate",
        "traits": "optimistic, sharp",
        "quirk": "Frequently underestimated, but turns out to be correct."
    },
    {
        "name": "MacGyver",
        "skills": ["rapid-prototyping", "resourcefulness", "chemistry", "systems-design"],
        "experience": 10,
        "availability": "2 weeks",
        "traits": "calm, improviser",
        "quirk": "Can fix outages with duct tape and a paperclip."
    },
    {
        "name": "Sheldon C.",
        "skills": ["theoretical-analysis", "pattern-recognition", "research"],
        "experience": 9,
        "availability": "Immediate",
        "traits": "rigid, brilliant",
        "quirk": "Correct 95% of the time and insufferable 100% of the time."
    },
    {
        "name": "Katniss E.",
        "skills": ["precision", "strategy", "crisis-management"],
        "experience": 5,
        "availability": "Immediate",
        "traits": "resilient, decisive",
        "quirk": "Excellent under pressure, poor at public speaking."
    },
    {
        "name": "Michael S.",
        "skills": ["sales", "public-speaking", "team-building"],
        "experience": 11,
        "availability": "Not looking",
        "traits": "enthusiastic, chaotic",
        "quirk": "Owns a best-boss mug."
    },
    {
        "name": "Olivia P.",
        "skills": ["crisis-management", "negotiation", "strategy", "leadership"],
        "experience": 13,
        "availability": "2 weeks",
        "traits": "decisive, intense",
        "quirk": "Handles it."
    },
    {
        "name": "Ted L.",
        "skills": ["team-building", "optimism", "mentorship", "public-speaking"],
        "experience": 7,
        "availability": "Immediate",
        "traits": "empathetic, persistent",
        "quirk": "Turns setbacks into folksy metaphors."
    },
    {
        "name": "Miranda P.",
        "skills": ["leadership", "negotiation", "stakeholder-management", "precision"],
        "experience": 18,
        "availability": "Not looking",
        "traits": "demanding, decisive",
        "quirk": "Reviews every pull request, making everyone panic."
    },
    {
        "name": "Dwight S.",
        "skills": ["sales", "negotiation", "security", "loyalty"],
        "experience": 9,
        "availability": "Immediate",
        "traits": "intense, loyal",
        "quirk": "Assistant to the regional backend engineer."
    }
]


JOBS = [
    {
        "title": "Backend Detective",
        "skills": ["deduction", "pattern-recognition", "forensics"],
        "minimum_experience": 3,
        "culture": "analytical, autonomous",
        "tagline": "We have a bug. We have no leads. We have you."
    },
    {
        "title": "Rapid Prototyping Engineer",
        "skills": ["rapid-prototyping", "systems-design"],
        "minimum_experience": 2,
        "culture": "innovative, fast-paced",
        "tagline": "Ship first, document never (kidding — please document)."
    },
    {
        "title": "Developer Relations Lead",
        "skills": ["public-speaking", "research"],
        "minimum_experience": 2,
        "culture": "energetic, curious",
        "tagline": "Explain complex things to confused humans cheerfully."
    },
    {
        "title": "Engineering Manager, Chaos Team",
        "skills": ["team-building", "stakeholder-management", "leadership"],
        "minimum_experience": 5,
        "culture": "empathetic, organized",
        "tagline": "Herd cats and senior engineers."
    },
    {
        "title": "Incident Commander",
        "skills": ["crisis-management", "strategy", "negotiation"],
        "minimum_experience": 4,
        "culture": "decisive, calm-under-pressure",
        "tagline": "It's 3 a.m. You're the one getting paged."
    },
    {
        "title": "Sales Engineer",
        "skills": ["sales", "public-speaking", "negotiation"],
        "minimum_experience": 3,
        "culture": "enthusiastic, persistent",
        "tagline": "Sell the vision, then build it."
    }
]


def seed_database():
    initialize_database()
    connection = get_connection()
    cursor = connection.cursor()

    for candidate in CANDIDATES:
        cursor.execute(
            "SELECT id FROM candidates WHERE name = ?",
            (candidate["name"],)
        )
        row = cursor.fetchone()

        if row:
            candidate_id = row["id"]
        else:
            cursor.execute("""
                INSERT INTO candidates
                (name, experience_years, availability, traits, quirk)
                VALUES (?, ?, ?, ?, ?)
            """, (
                candidate["name"],
                candidate["experience"],
                candidate["availability"],
                candidate["traits"],
                candidate["quirk"]
            ))
            candidate_id = cursor.lastrowid

        for skill in candidate["skills"]:
            cursor.execute("""
                INSERT OR IGNORE INTO candidate_skills
                (candidate_id, skill)
                VALUES (?, ?)
            """, (candidate_id, skill))

    for job in JOBS:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs
            (title, minimum_experience, culture, tagline)
            VALUES (?, ?, ?, ?)
        """, (
            job["title"],
            job["minimum_experience"],
            job["culture"],
            job["tagline"]
        ))

        cursor.execute(
            "SELECT id FROM jobs WHERE title = ?",
            (job["title"],)
        )
        job_id = cursor.fetchone()["id"]

        for skill in job["skills"]:
            cursor.execute("""
                INSERT OR IGNORE INTO job_required_skills
                (job_id, skill)
                VALUES (?, ?)
            """, (job_id, skill))

    connection.commit()

    candidate_count = cursor.execute(
        "SELECT COUNT(*) FROM candidates"
    ).fetchone()[0]

    job_count = cursor.execute(
        "SELECT COUNT(*) FROM jobs"
    ).fetchone()[0]

    connection.close()

    print("Seed data inserted successfully.")
    print(f"Candidates in database: {candidate_count}")
    print(f"Jobs in database: {job_count}")


if __name__ == "__main__":
    seed_database()