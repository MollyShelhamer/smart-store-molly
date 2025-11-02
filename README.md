# Pro Analytics — smart-store-molly

Minimal, professional starter for analytics projects using Python.
This repo contains demo modules, logging helpers, tests, and docs to
help you build reproducible analytics workflows.

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
- Tests (smoke): tests/test_smoke.py
- License: LICENSE

## Prerequisites
- Python 3.10+ (3.12 recommended)
- Git
- VS Code (recommended)

## Quick start (local)
1. Clone the repo and open the project folder in VS Code.
2. Create and activate a virtual environment:
```powershell
py -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin\activate

Install dependencies:

py -m pip install --upgrade pippy -m pip install -r requirements.txt
Run demo modules
From the project root:


python -m analytics_project.demo_module_basicspython -m analytics_project.demo_module_statspython -m analytics_project.demo_module_vizpython -m analytics_project.demo_module_languages# Or run the orchestrator:python -m analytics_project.main
Tests
Run the test suite with pytest:


pytest -q
Daily workflow (common commands)

git pull# update deps (project uses uv / uvx helper tooling if available)uv sync --extra dev --extra docs --upgradeuvx ruff check --fixuv run pre-commit run --all-filespytest
Docs
Build and serve docs locally:


uv run mkdocs build --strictuv run mkdocs serve
Notes
Logging is configured via src/analytics_project/utils_logger.py.
Follow STRUCTURE.md when adding code, data, notebooks, and tests.
Use small, frequent commits and push to GitHub to preserve progress.

