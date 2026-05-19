import argparse
import hashlib
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


DEFAULT_SCHEMA_FILE = "schema.sql"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load cleaned review data into PostgreSQL using the project schema."
    )
    parser.add_argument("--input", required=True, help="Path to the cleaned review CSV file.")
    parser.add_argument("--db-user", default="postgres", help="Postgres username.")
    parser.add_argument("--db-password", default="postgres", help="Postgres password.")
    parser.add_argument("--db-host", default="localhost", help="Postgres host.")
    parser.add_argument("--db-port", default="5432", help="Postgres port.")
    parser.add_argument("--db-name", default="bank_reviews", help="Postgres database name.")
    parser.add_argument(
        "--schema-file",
        default=DEFAULT_SCHEMA_FILE,
        help="Path to the PostgreSQL schema SQL file.",
    )
    return parser.parse_args()


def build_engine(user: str, password: str, host: str, port: str, database: str):
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


def load_data(path: str) -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)
    if "review_id" not in df.columns:
        df["review_id"] = df.apply(
            lambda row: hashlib.sha1(str(row["review_text"]).encode("utf-8")).hexdigest(),
            axis=1,
        )

    if "bank_id" not in df.columns and "bank_name" in df.columns:
        df["bank_id"] = (
            df["bank_name"].astype(str)
            .str.lower()
            .str.replace(r"[^a-z0-9]+", "_", regex=True)
            .str.strip("_")
        )

    if "review_date" in df.columns:
        df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    for col in ["sentiment_score", "rating"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def create_schema(engine, schema_file: str):
    if not Path(schema_file).exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    sql = Path(schema_file).read_text()
    with engine.begin() as conn:
        conn.execute(text(sql))


def insert_banks(engine, df: pd.DataFrame):
    required = ["bank_id", "bank_name", "app_name"]
    if not all(col in df.columns for col in required):
        raise ValueError(f"Input file must contain {required}")

    banks = df[required].drop_duplicates().to_dict(orient="records")
    insert_sql = text(
        "INSERT INTO banks (bank_id, bank_name, app_name) VALUES (:bank_id, :bank_name, :app_name) "
        "ON CONFLICT (bank_id) DO UPDATE SET bank_name = EXCLUDED.bank_name, app_name = EXCLUDED.app_name"
    )
    with engine.begin() as conn:
        for row in banks:
            conn.execute(insert_sql, **row)


def insert_reviews(engine, df: pd.DataFrame):
    required = [
        "review_id",
        "bank_id",
        "review_text",
        "rating",
        "review_date",
        "sentiment_label",
        "sentiment_score",
        "identified_theme",
        "source",
    ]
    if not all(col in df.columns for col in required):
        raise ValueError(f"Input file must contain {required}")

    reviews = df[required].fillna("").to_dict(orient="records")
    insert_sql = text(
        "INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source) "
        "VALUES (:review_id, :bank_id, :review_text, :rating, :review_date, :sentiment_label, :sentiment_score, :identified_theme, :source) "
        "ON CONFLICT (review_id) DO NOTHING"
    )
    with engine.begin() as conn:
        for row in reviews:
            conn.execute(insert_sql, **row)


def main():
    args = parse_args()
    df = load_data(args.input)
    engine = build_engine(args.db_user, args.db_password, args.db_host, args.db_port, args.db_name)

    print(f"Creating schema from {args.schema_file} if needed...")
    create_schema(engine, args.schema_file)
    print("Inserting bank metadata...")
    insert_banks(engine, df)
    print("Inserting review records...")
    insert_reviews(engine, df)
    print("Data ingestion complete.")


if __name__ == "__main__":
    main()
