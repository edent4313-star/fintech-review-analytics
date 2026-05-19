CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),

    review_text TEXT,
    rating INTEGER,
    review_date DATE,

    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,

    identified_theme VARCHAR(100),

    source VARCHAR(50)
);

Count Reviews Per Bank

SELECT b.bank_name,
       COUNT(r.review_id) AS total_reviews
FROM banks b
JOIN reviews r
ON b.bank_id = r.bank_id
GROUP BY b.bank_name;


Average Rating

SELECT b.bank_name,
       AVG(r.rating) AS avg_rating
FROM banks b
JOIN reviews r
ON b.bank_id = r.bank_id
GROUP BY b.bank_name;


Check Nulls

SELECT *
FROM reviews
WHERE review_text IS NULL
   OR rating IS NULL
   OR sentiment_label IS NULL;