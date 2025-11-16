# Pro Analytics — smart-store-molly

Minimal, professional starter for analytics projects using Python.  
This repo contains ETL scripts, data prep utilities, logging helpers, tests, and docs to help you build reproducible analytics workflows.

## Quick Links
- Package entry: `analytics_project.main` (src/analytics_project/main.py)
- Demo modules:
  - `analytics_project.demo_module_basics`
  - `analytics_project.dw.etl_to_dw`
  - `analytics_project.data_prep`
  - `analytics_project.data_scrubber`

## How to Run
Create and activate a virtual environment:
```
uv venv
uv pip install -r requirements.txt
```

Run data prep:
```
uv run python -m analytics_project.data_prep
```

Run the DW load:
```
uv run python -m analytics_project.dw.etl_to_dw
```

Run the demo:
```
uv run python -m analytics_project.main
```

## Data Prep (data_prep.py)
Performs:

- Duplicate removal
- String cleanup (upper + trimmed)
- Missing text fields → "UNKNOWN"
- Column normalization to snake_case
- **Preserves numeric identifiers (e.g. CampaignID)**

## Data Warehouse
Cleaned data is moved to data/warehouse/smart_sales.db using etl_to_dw.py

## Data Warehouse Schema Overview

### **Dimension Tables**
#### `customer`
| Column         | Type    |
|----------------|---------|
| customer_id    | INT PK  |
| first_name     | TEXT    |
| last_name      | TEXT    |
| email          | TEXT    |
| city           | TEXT    |
| state          | TEXT    |
| join_date      | DATE    |

#### `product`
| Column        | Type    |
|---------------|---------|
| product_id    | INT PK  |
| product_name  | TEXT    |
| category      | TEXT    |
| price         | NUMERIC |

### **Fact Table**
#### `sale`
| Column         | Type        |
|----------------|-------------|
| sale_id        | INT PK      |
| sale_date      | DATE        |
| customer_id    | INT FK      |
| product_id     | INT FK      |
| campaign_id    | INT FK NULL |
| quantity       | INT         |
| total_amount   | NUMERIC     |

## Logging
Uses `loguru` for structured logging:
```
2025-11-15 12:56:30.386 | INFO | data_prep: Loaded customers_data.csv
```

## Development
Format code:
```
uv run ruff format .
```

Run tests:
```
uv run pytest
```
