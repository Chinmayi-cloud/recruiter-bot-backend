
-- Question 1: List all open job postings with their recruiter names.
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    jp.department,
    jp.opened_date,
    r.name AS recruiter_name,
    r.region
FROM job_postings AS jp
JOIN recruiters AS r
    ON jp.recruiter_id = r.id
WHERE jp.status = 'open'
ORDER BY jp.id;


-- Question 2: Count applicants reaching the Final stage for each job posting.
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    COUNT(DISTINCT i.applicant_id) AS applicants_reaching_final
FROM job_postings AS jp
LEFT JOIN interviews AS i
    ON jp.id = i.job_posting_id
    AND i.stage = 'Final'
GROUP BY jp.id, jp.title
ORDER BY jp.id;


-- Question 3: Find people who effectively applied to more than one job.
-- Normalize email casing and whitespace to identify duplicate applicant records.
SELECT
    MIN(a.full_name) AS applicant_name,
    LOWER(TRIM(a.email)) AS normalized_email,
    COUNT(DISTINCT i.job_posting_id) AS distinct_jobs,
    GROUP_CONCAT(DISTINCT i.job_posting_id) AS job_ids
FROM applicants AS a
JOIN interviews AS i
    ON a.id = i.applicant_id
GROUP BY LOWER(TRIM(a.email))
HAVING COUNT(DISTINCT i.job_posting_id) > 1
ORDER BY distinct_jobs DESC, applicant_name;


-- Question 4: Calculate Final-stage conversion per recruiter.
-- Include only recruiters with at least 3 Final-stage interviews.
SELECT
    r.id AS recruiter_id,
    r.name AS recruiter_name,
    COUNT(*) AS total_final_interviews,
    SUM(CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END)
        AS passed_final_interviews,
    ROUND(
        100.0 * SUM(CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS final_conversion_percentage
FROM recruiters AS r
JOIN job_postings AS jp
    ON r.id = jp.recruiter_id
JOIN interviews AS i
    ON jp.id = i.job_posting_id
WHERE i.stage = 'Final'
GROUP BY r.id, r.name
HAVING COUNT(*) >= 3
ORDER BY final_conversion_percentage DESC, r.name;


-- Question 5 (Bonus): Find the recruiter(s) with the most
-- successful placements in each department using a window function.
-- A successful placement is a Final-stage interview with outcome 'passed'.
WITH recruiter_placements AS (
    SELECT
        jp.department,
        r.id AS recruiter_id,
        r.name AS recruiter_name,
        COUNT(
            CASE
                WHEN i.stage = 'Final' AND i.outcome = 'passed'
                THEN 1
            END
        ) AS successful_placements
    FROM job_postings AS jp
    JOIN recruiters AS r
        ON jp.recruiter_id = r.id
    LEFT JOIN interviews AS i
        ON jp.id = i.job_posting_id
    GROUP BY jp.department, r.id, r.name
),
ranked_recruiters AS (
    SELECT
        department,
        recruiter_id,
        recruiter_name,
        successful_placements,
        RANK() OVER (
            PARTITION BY department
            ORDER BY successful_placements DESC
        ) AS placement_rank
    FROM recruiter_placements
)
SELECT
    department,
    recruiter_id,
    recruiter_name,
    successful_placements
FROM ranked_recruiters
WHERE placement_rank = 1
ORDER BY department;
