-- PostgreSQL schema for fintech review analytics

CREATE TABLE banks (
    bank_id TEXT PRIMARY KEY,
    bank_name TEXT NOT NULL,
    app_name TEXT NOT NULL
);

CREATE TABLE reviews (
    review_id TEXT PRIMARY KEY,
    bank_id TEXT NOT NULL REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    sentiment_label TEXT,
    sentiment_score NUMERIC(4,3),
    identified_theme TEXT,
    source TEXT NOT NULL DEFAULT 'Google Play'
);

CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_review_date ON reviews(review_date);
