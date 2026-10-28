import sqlite3

DATABASE_NAME = "recruiter_bot.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the candidates and jobs tables."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            experience_years INTEGER NOT NULL,
            availability TEXT NOT NULL,
            traits TEXT NOT NULL,
            quirk TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            minimum_experience INTEGER NOT NULL,
            culture TEXT NOT NULL,
            tagline TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate_skills (
            candidate_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            PRIMARY KEY (candidate_id, skill),
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_required_skills (
            job_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            PRIMARY KEY (job_id, skill),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database tables created successfully.")