# Scripts
This directory contains utility scripts for the fintech review analytics pipeline.

- `scrape_reviews.py`: Live scraping from Google Play Store.
- `task_2_analysis.py`: Performs sentiment and thematic analysis on raw data.
- # Fintech Review Analytics

This repository contains a comprehensive pipeline for analyzing customer reviews of fintech applications. It uses Natural Language Processing (NLP) to extract sentiments, themes, and business insights.

## Project Structure
```text
fintech-review-analytics/
├── .vscode/               # Editor settings
├── .github/workflows/      # CI/CD (Unit tests)
├── data/                   # Data directory (gitignored *.csv)
│   └── raw/               # Raw review data
├── notebooks/             # Exploratory analysis & Demos
├── src/                   # Source code (modular logic)
├── tests/                 # Unit tests
├── scripts/               # Production scripts
└── requirements.txt       # Dependencies
```

## Getting Started
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the data collection and preprocessing:
   ```bash
   python scripts/scrape_reviews.py
   python scripts/preprocess_data.py
   ```

## Task 1: Data Collection and Preprocessing

### Scraping Methodology
- **Library**: `google-play-scraper`
- **Targets**: 
  - Telebirr (`cn.tydic.ethiopay`)
  - CBE Birr (`prod.cbe.birr`)
  - Bank of Abyssinia Apollo (`com.boa.apollo`)
- **Parameters**: Collected all available reviews with `country='et'` and `lang='en'`.
- **Date Range**: 2020-08-06 to 2026-05-13.
- **Fields Collected**: Review text, rating (1–5), review date, bank name, source ("Google Play").

### Preprocessing Steps
1. **Deduplication**: Removed duplicate reviews based on content, bank, and date.
2. **Missing Value Handling**: Dropped rows missing review text or rating.
3. **Date Normalization**: Converted all dates to `YYYY-MM-DD` format.
4. **Export**: Saved cleaned dataset as `data/cleaned_reviews.csv`.

### KPIs Achieved
- **Volume**: 20,781+ reviews collected (Target: 1,200+).
- **Data Quality**: <1% missing data dropped during preprocessing.
- **Organization**: Clean CSV generated with all required columns.

## Key Features
- **Sentiment Analysis**: Comparative analysis using TextBlob, VADER, and DistilBERT.
- **Thematic Mapping**: Rule-based categorization of reviews into business themes (Stability, UX, Features, etc.).
- **Visual Analytics**: Distribution plots and theme-sentiment divergence charts.

## Error Handling & Testing
- Robust data loading with type checking and file existence verification.
- Unit tests for text preprocessing and sentiment logic in the `tests/` directory.
- Automated testing via GitHub Actions.
# Fintech Review Analytics

This repository contains a comprehensive pipeline for analyzing customer reviews of fintech applications. It uses Natural Language Processing (NLP) to extract sentiments, themes, and business insights.

## Project Structure
```text
fintech-review-analytics/
├── .vscode/               # Editor settings
├── .github/workflows/      # CI/CD (Unit tests)
├── data/                   # Data directory (gitignored *.csv)
│   └── raw/               # Raw review data
├── notebooks/             # Exploratory analysis & Demos
├── src/                   # Source code (modular logic)
├── tests/                 # Unit tests
├── scripts/               # Production scripts
└── requirements.txt       # Dependencies
```

## Getting Started
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the PostgreSQL database (optional for database ingestion):
   ```bash
   psql -U postgres -c "CREATE DATABASE bank_reviews;"
   psql -U postgres -d bank_reviews -f schema.sql
   ```
4. Install database drivers for Python if needed:
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```
5. Run the data collection and preprocessing:
   ```bash
   python scripts/scrape_reviews.py
   python scripts/preprocess_data.py
   ```

## Database Schema and Setup
The database schema is defined in `schema.sql` and supports two tables:
- `banks`
  - `bank_id` (PRIMARY KEY)
  - `bank_name`
  - `app_name`
- `reviews`
  - `review_id` (PRIMARY KEY)
  - `bank_id` (foreign key to `banks`)
  - `review_text`
  - `rating`
  - `review_date`
  - `sentiment_label`
  - `sentiment_score`
  - `identified_theme`
  - `source`

This project includes notebook ingestion logic in `notebooks/Task 3.ipynb`, which loads review data into `banks` and `reviews` using SQLAlchemy.

## Task 1: Data Collection and Preprocessing

### Scraping Methodology
- **Library**: `google-play-scraper`
- **Targets**: 
  - Telebirr (`cn.tydic.ethiopay`)
  - CBE Birr (`prod.cbe.birr`)
  - Bank of Abyssinia Apollo (`com.boa.apollo`)
- **Parameters**: Collected all available reviews with `country='et'` and `lang='en'`.
- **Date Range**: 2020-08-06 to 2026-05-13.
- **Fields Collected**: Review text, rating (1–5), review date, bank name, source ("Google Play").

### Preprocessing Steps
1. **Deduplication**: Removed duplicate reviews based on content, bank, and date.
2. **Missing Value Handling**: Dropped rows missing review text or rating.
3. **Date Normalization**: Converted all dates to `YYYY-MM-DD` format.
4. **Export**: Saved cleaned dataset as `data/cleaned_reviews.csv`.

### KPIs Achieved
- **Volume**: 20,781+ reviews collected (Target: 1,200+).
- **Data Quality**: <1% missing data dropped during preprocessing.
- **Organization**: Clean CSV generated with all required columns.

## Key Features
- **Sentiment Analysis**: Comparative analysis using TextBlob, VADER, and DistilBERT.
- **Thematic Mapping**: Rule-based categorization of reviews into business themes (Stability, UX, Features, etc.).
- **Visual Analytics**: Distribution plots and theme-sentiment divergence charts.

## Error Handling & Testing
- Robust data loading with type checking and file existence verification.
- Unit tests for text preprocessing and sentiment logic in the `tests/` directory.
- Automated testing via GitHub Actions.


