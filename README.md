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
