# Internship Management CLI

A simple Flask + SQLAlchemy command‑line interface (CLI) to manage **students**, **staff**, **employers**, and **internship positions** for a basic internship shortlist workflow.

---

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

---

## Setup

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Tell Flask where the app is**

- **Windows (PowerShell)**
  ```powershell
  $env:FLASK_APP="wsgi:app"
  ```
- **Linux / macOS**
  ```bash
  export FLASK_APP=wsgi:app
  ```

3. **Initialize database (creates tables + seeds demo data)**

```bash
flask reset-db   # Drops and recreates all tables
flask init-db    # Creates tables and seeds: students, staff, employers, positions
```

> Seeded demo data includes:
>
> - Staff: **Bob**, **Rob**
> - Students: **Alice**, **Erina**
> - Employers: **Totsuki Culinary Academy**, **Central Inc.**
> - Positions: **Web Development Intern** (Totsuki), **Data Analyst Intern** (Central)

---

## CLI Commands

### Students

**Create a student**

```bash
flask student create <name>
```

Example:

```bash
flask student create John
```

Notes: Names are unique. If the name exists you will see an error.

**View a student’s shortlist entries**

```bash
flask student my-shortlists <student_name>
```

Example:

```bash
flask student my-shortlists John
```

---

### Staff

**Create a staff member**

```bash
flask staff create <name>
```

Example:

```bash
flask staff create Tom
```

Notes: Names are unique.

**List all staff**

```bash
flask staff list
```

**Shortlist a student for a position (by staff)**

```bash
flask staff shortlist-add <staff_id> <student_name> <position_id>
```

Example:

```bash
flask staff shortlist-add 1 John 2
```

- `staff_id`: numeric id (see `flask staff list`)
- `student_name`: exact student name (e.g., `John`)
- `position_id`: numeric id (see employer list commands below)

---

### Employers

**Create an employer**

```bash
flask employer create <company>
```

Example:

```bash
flask employer create "Tech Corp"
```

Notes: Company names are unique.

**Create a position for an employer**

```bash
flask employer create-position <company> <title> <description>
```

Example:

```bash
flask employer create-position "Tech Corp" "Backend Intern" "Work with APIs"
```

**List positions (all or by company)**

```bash
flask employer list
flask employer list <company>
```

Examples:

```bash
flask employer list
flask employer list "Tech Corp"
```

**View shortlist for a specific position (must belong to that company)**

```bash
flask employer shortlist <company> <position_id>
```

Example:

```bash
flask employer shortlist "Central Inc." 2
```

**Accept a student from a shortlist (must belong to that company)**

```bash
flask employer accept <company> <shortlist_id>
```

Example:

```bash
flask employer accept "Central Inc." 1
```

**Reject a student from a shortlist (must belong to that company)**

```bash
flask employer reject <company> <shortlist_id>
```

Example:

```bash
flask employer reject "Central Inc." 1
```

> If a company tries to accept/reject a shortlist that **doesn’t belong** to one of its positions, the command prints an error and **does nothing**.

---

## Sample Workflow (Copy/Paste Demo)

> This walkthrough starts from a clean database and shows a full cycle: seed → add users → create employer+position → shortlist → accept/reject → student views status.

### Windows (PowerShell)

```powershell
# 1) Set Flask app (one time per session)
$env:FLASK_APP="wsgi:app"

# 2) Reset + Seed demo data
flask reset-db
flask init-db

# 3) Quick checks
flask staff list
flask employer list
flask student my-shortlists John   # John not seeded yet -> should print error

# 4) Create extra users + employer + position
flask student create John
flask staff create Tom
flask employer create "Tech Corp"
flask employer create-position "Tech Corp" "Backend Intern" "Work with APIs"

# 5) List positions (show all + filter by company)
flask employer list
flask employer list "Tech Corp"

# 6) Shortlist John to seeded position #2 (Central Inc.) by Staff #1 (Bob)
flask staff shortlist-add 1 John 2

# 7) View shortlist (correct employer vs mismatch)
flask employer shortlist "Central Inc." 2     # Shows John (PENDING)
flask employer shortlist "Tech Corp" 2        # Prints: That position does not belong to this company.

# 8) Accept with WRONG employer (should only print error, no change)
flask employer accept "Tech Corp" 1

# 9) Accept with CORRECT employer
flask employer accept "Central Inc." 1

# 10) Student sees ACCEPTED
flask student my-shortlists John

# 11) Reject (correct employer) — to show both statuses in action
flask employer reject "Central Inc." 1

# 12) Student sees REJECTED
flask student my-shortlists John

# 13) Some error paths (duplicates / bad ids)
flask student create Alice              # duplicate student
flask staff create Bob                  # duplicate staff
flask employer create "Central Inc."    # duplicate employer
flask employer accept "Tech Corp" 999   # non-existent shortlist
flask employer shortlist "Tech Corp" 999# non-existent position
```

### Linux / macOS (bash/zsh)

```bash
# 1) Set Flask app
export FLASK_APP=wsgi:app

# 2) Reset + Seed demo data
flask reset-db
flask init-db

# 3) Quick checks
flask staff list
flask employer list
flask student my-shortlists John || true

# 4) Create extra users + employer + position
flask student create John
flask staff create Tom
flask employer create "Tech Corp"
flask employer create-position "Tech Corp" "Backend Intern" "Work with APIs"

# 5) List positions
flask employer list
flask employer list "Tech Corp"

# 6) Shortlist John to seeded position #2 (Central Inc.) by Staff #1 (Bob)
flask staff shortlist-add 1 John 2

# 7) View shortlist
flask employer shortlist "Central Inc." 2
flask employer shortlist "Tech Corp" 2 || true

# 8) Wrong employer try (no change)
flask employer accept "Tech Corp" 1 || true

# 9) Correct employer accept
flask employer accept "Central Inc." 1

# 10) Student sees ACCEPTED
flask student my-shortlists John

# 11) Reject (correct employer)
flask employer reject "Central Inc." 1

# 12) Student sees REJECTED
flask student my-shortlists John

# 13) Error paths
flask student create Alice || true
flask staff create Bob || true
flask employer create "Central Inc." || true
flask employer accept "Tech Corp" 999 || true
flask employer shortlist "Tech Corp" 999 || true.
```

---

## Notes

- Use quotes for company names or titles with spaces (e.g., `"Tech Corp"`, `"Central Inc."`).
- Uniqueness is enforced for student names, staff names, and employer company names.
- The CLI prints friendly errors and avoids crashing on common mistakes.
