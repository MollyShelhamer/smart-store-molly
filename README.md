# Pro Analytics — smart-store-molly

Minimal, professional starter for analytics projects using Python.  
This repo contains demo modules, logging helpers, tests, and docs to help you build reproducible analytics workflows.

---

## Quick links
- Package entry: `analytics_project.main` (src/analytics_project/main.py)  
- Demo modules:
  - `analytics_project.demo_module_basics` (src/analytics_project/demo_module_basics.py)
  - `analytics_project.demo_module_stats` (src/analytics_project/demo_module_stats.py)
  - `analytics_project.demo_module_viz` (src/analytics_project/demo_module_viz.py)
  - `analytics_project.demo_module_languages` (src/analytics_project/demo_module_languages.py)
- Logger helper: `analytics_project.utils_logger` (src/analytics_project/utils_logger.py)
- Optional data prep example: `analytics_project.data_prep` (src/analytics_project/data_prep.py)
- Project structure: STRUCTURE.md
- Tests (smoke): `tests/test_smoke.py`
- License: LICENSE

---

## Prerequisites
- Python **3.10+** (3.12 recommended)  
- Git  
- VS Code (recommended)

---

## Quick start (local)

### 1. Clone the repo & open in VS Code
```bash
git clone <your-repo-url>
cd <repo-name>
code .
```

### 2. Create and activate a virtual environment
```powershell
# Create venv
py -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\activate

# Activate (macOS / Linux)
source .venv/bin/activate
```

### 3. Install dependencies
```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

---

## Run demo modules

From the project root:

```bash
python -m analytics_project.demo_module_basics
python -m analytics_project.demo_module_stats
python -m analytics_project.demo_module_viz
python -m analytics_project.demo_module_languages
```

Or run the orchestrator:

```bash
python -m analytics_project.main
```

---

## Daily workflow (common commands)

```bash
git pull

# Update dependencies (if using uv / uvx)
uv sync --extra dev --extra docs --upgrade

uvx ruff check --fix
uv run pre-commit run --all-files

pytest
```

---

## Notes
- Logging is configured via `src/analytics_project/utils_logger.py`.  
- Follow STRUCTURE.md when adding code, data, notebooks, and tests.  
- Use small, frequent commits and push to GitHub to preserve progress.

