# Internship Management CLI

This project provides a simple Flask + SQLAlchemy command-line interface (CLI) to manage **students**, **staff**, **employers**, and **internship positions**.

---

## Setup

1. Clone the repository and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set the Flask app environment variable:

   **Windows (PowerShell):**
   ```powershell
   $env:FLASK_APP="wsgi:app"
   ```

   **Linux/Mac (bash/zsh):**
   ```bash
   export FLASK_APP=wsgi:app
   ```

3. Initialize or reset the database:

   ```bash
   flask reset-db   # Drops and recreates all tables
   flask init-db    # Creates tables and seeds initial data
   ```

---

## Commands

### Student Commands

**Create a student**
```bash
flask student create <name>
```
Example:
```bash
flask student create John
```

**View a student’s shortlists**
```bash
flask student my-shortlists <student_name>
```
Example:
```bash
flask student my-shortlists John
```

---

### Staff Commands

**Create a staff member**
```bash
flask staff create <name>
```
Example:
```bash
flask staff create Alice
```

**List all staff**
```bash
flask staff list
```

**Shortlist a student for a position**
```bash
flask staff shortlist-add <staff_id> <student_name> <position_id>
```
Example:
```bash
flask staff shortlist-add 1 John 2
```

---

### Employer Commands

**Create an employer**
```bash
flask employer create <company>
```
Example:
```bash
flask employer create "Tech Corp"
```

**Create a position for an employer**
```bash
flask employer create-position <company> <title> <description>
```
Example:
```bash
flask employer create-position "Tech Corp" "Backend Intern" "Work with APIs"
```

**List positions**
```bash
flask employer list
flask employer list <company>
```
Examples:
```bash
flask employer list
flask employer list "Tech Corp"
```

**View shortlist for a position**
```bash
flask employer shortlist <company> <position_id>
```
Example:
```bash
flask employer shortlist "Tech Corp" 3
```

**Accept a student from a shortlist**
```bash
flask employer accept <company> <shortlist_id>
```
Example:
```bash
flask employer accept "Tech Corp" 1
```

**Reject a student from a shortlist**
```bash
flask employer reject <company> <shortlist_id>
```
Example:
```bash
flask employer reject "Tech Corp" 1
```
