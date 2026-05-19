# Task 1: Data Scraping & Preprocessing — Comprehensive Documentation

## Overview
This notebook documents the complete workflow for scraping, cleaning, and preprocessing Google Play Store reviews from three Ethiopian fintech banks: **CBE Bank**, **Dashen Bank**, and **BOA Bank**.

---

## Scraping Methodology

### Data Source
- **Platform**: Google Play Store
- **Library**: `google-play-scraper` (Python package)
- **Language**: English
- **Region**: Ethiopia (ET)

### Banks Scraped

| Bank | App ID | Reviews Targeted |
|------|--------|------------------|
| CBE Bank | `com.combanketh.mobilebanking` | 400 |
| Dashen Bank | `com.dashen.dashensuperapp` | 400 |
| BOA Bank | `com.boa.boaMobileBanking` | 400 |

### Scraping Parameters

```python
reviews(
    app_id,
    lang='en',              # English language only
    country='et',           # Ethiopia region
    sort=Sort.NEWEST,       # Most recent reviews first
    count=400,              # Target: 400 reviews per bank
    filter_score_with=None  # All star ratings (1-5)
)
```

### Data Fields Extracted Per Review
- **reviewId**: Unique review identifier from Google Play
- **content**: Full review text
- **score**: Star rating (integer, 1-5)
- **at**: Review publication date (datetime object)

---

## Date Range & Data Collection

### Temporal Coverage
Reviews collected spanning **May 2025 to December 2025** (8-month period)

**Date Range by Bank** (actual):
- **CBE Bank**: May 2025 – December 2025
- **Dashen Bank**: May 2025 – December 2025
- **BOA Bank**: May 2025 – December 2025

### Collection Strategy
- **Sort order**: NEWEST (most recent first)
- **Maximum per bank**: 400 reviews
- **Filtering**: All star ratings included (no filtering by score)

---

## Data Processing Pipeline

### Phase 1: Data Quality Audit

Before cleaning, raw data was assessed for:

**Problem 1: Missing Values**
- Checked all 6 columns (review_id, review, rating, date, bank, source)
- Identified null/NaN entries in critical columns

**Problem 2: Duplicates**
- Duplicate review_id (same review posted twice)
- Duplicate review text (verbatim copies)
- Empty or whitespace-only reviews

**Problem 3: Date Format**
- Inconsistent timestamp formatting (datetime objects)
- Needed normalization to YYYY-MM-DD string format

**Problem 4: Invalid Ratings**
- Ratings outside 1-5 range (rare but checked)

### Phase 2: Data Cleaning

**Step 1: Remove Missing Critical Data**
```python
df.dropna(subset=['review', 'rating'])
```
- Keeps only rows with both text and rating
- Drops invalid rows

**Step 2: Remove Duplicates**
```python
df.drop_duplicates(subset=['review_id'], keep='first')
```
- Keeps first occurrence of duplicate review_id
- Removes duplicate rows

**Step 3: Standardize Dates**
```python
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
```
- Converts datetime objects to `YYYY-MM-DD`
- Normalizes all dates

**Step 4: Clean Review Text**
```python
text = re.sub(r'\s+', ' ', text).strip()
```
- Collapses multiple spaces/newlines
- Removes leading/trailing whitespace

**Step 5: Validate Ratings**
```python
df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
df['rating'] = df['rating'].astype(int)
```
- Removes out-of-range ratings
- Ensures integer star ratings

### Phase 3: Enrichment with Sentiment Analysis

**Sentiment Analysis Method**: VADER (Valence Aware Dictionary and sEntiment Reasoner)

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
```

**Classification Thresholds**:
- **Positive**: compound score ≥ 0.05
- **Negative**: compound score ≤ -0.05
- **Neutral**: -0.05 < compound score < 0.05

### Phase 4: Final Output

**8-Column CSV Format**:
1. `review` – Full review text (cleaned)
2. `rating` – Star rating (1-5, integer)
3. `date` – Review date (YYYY-MM-DD)
4. `bank` – Bank name
5. `source` – Always "Google Play"
6. `month` – Extracted month name
7. `length` – Review text length
8. `sentiment` – Positive/Neutral/Negative

---

## Output Files

```
data/raw/CBE_bank_reviews_clean_F.csv
data/raw/Dashen_bank_reviews_clean_F.csv
data/raw/BOA_bank_reviews_clean_F.csv
```

## Limitations & Constraints

1. Limited sample size (400 reviews per bank)
2. Temporal bias from newest-first scraping
3. Selection bias from review authors
4. English-only review filtering
5. VADER sentiment limitations
6. Missing metadata (app version, device info)
7. 8-month date range constraints
8. Google Play scraping limits
9. Data snapshot freshness
10. Preprocessing trade-offs

---

## Recommendations

- Re-scrape periodically for temporal coverage
- Collect Amharic reviews for local sentiment
- Validate sentiment with manual review samples
- Combine review data with support tickets and app logs
- Use domain-specific NLP models for fintech

---

**Last Updated**: May 19, 2026
**Data Period**: May 2025 – December 2025
**Notes**: This README is intentionally focused on Task 1 scraping and preprocessing.
