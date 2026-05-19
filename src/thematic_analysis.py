import re
from collections import Counter
from typing import Dict, List, Optional

# Business theme mapping that supports fintech review analysis.
THEME_MAP: Dict[str, List[str]] = {
    "Account Access": [
        "login",
        "account",
        "password",
        "pin",
        "signin",
        "sign in",
        "signing in",
        "signing out",
        "locked",
        "unlock",
        "reset password",
    ],
    "Transaction": [
        "transfer",
        "payment",
        "send money",
        "receive",
        "deposit",
        "withdraw",
        "transaction",
        "payment failed",
        "transfer failed",
        "balance",
        "funds",
    ],
    "Stability & Performance": [
        "crash",
        "slow",
        "lag",
        "timeout",
        "freeze",
        "loading",
        "error",
        "bug",
        "unresponsive",
        "hang",
    ],
    "Update & Compatibility": [
        "update",
        "version",
        "compatibility",
        "android",
        "ios",
        "apk",
        "install",
        "compatible",
        "new version",
    ],
    "Customer Support": [
        "support",
        "help",
        "customer service",
        "agent",
        "chat",
        "call",
        "ticket",
        "response",
    ],
    "Security & Trust": [
        "secure",
        "security",
        "fraud",
        "otp",
        "authentication",
        "privacy",
        "trusted",
        "unauthorized",
        "biometric",
    ],
    "Usability & UX": [
        "easy",
        "difficult",
        "user friendly",
        "ui",
        "ux",
        "navigate",
        "navigation",
        "interface",
        "confusing",
        "experience",
        "design",
        "layout",
    ],
    "Feature Requests": [
        "feature",
        "wish",
        "need",
        "request",
        "add",
        "improve",
        "option",
        "functionality",
    ],
}


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_primary_theme(text: str, theme_map: Optional[Dict[str, List[str]]] = None) -> str:
    """Return the most likely business theme for a review text."""
    theme_map = theme_map or THEME_MAP
    txt = normalize_text(text)
    if not txt:
        return "Other"

    counts: Dict[str, int] = {}
    for theme, keywords in theme_map.items():
        score = 0
        for keyword in keywords:
            if keyword in txt:
                score += txt.count(keyword)
        if score > 0:
            counts[theme] = score

    if not counts:
        return "Other"

    best_theme = max(counts, key=counts.get)
    return best_theme


def assign_themes(reviews: List[str], theme_map: Optional[Dict[str, List[str]]] = None) -> List[str]:
    return [get_primary_theme(text, theme_map=theme_map) for text in reviews]


def theme_summary(df, review_col: str = "review", theme_col: str = "identified_theme", sentiment_col: str = "sentiment_score"):
    """Return a theme-level summary for the dataset."""
    if theme_col not in df.columns:
        df[theme_col] = assign_themes(df[review_col].astype(str).tolist())

    summary = df.groupby(theme_col)[sentiment_col].agg(["count", "mean"]).sort_values(by="count", ascending=False)
    return summary


def top_themes_by_bank(df, bank_col: str = "bank_name", theme_col: str = "identified_theme", sentiment_col: str = "sentiment_score", top_n: int = 3):
    """Return the strongest positive and negative themes by bank."""
    if theme_col not in df.columns:
        raise ValueError(f"Missing theme column: {theme_col}")

    results = {}
    for bank, group in df.groupby(bank_col):
        theme_stats = group.groupby(theme_col)[sentiment_col].mean().sort_values(ascending=False)
        positive = theme_stats.head(top_n).to_dict()
        negative = theme_stats.tail(top_n).to_dict()
        results[bank] = {
            "positive_themes": positive,
            "negative_themes": negative,
        }
    return results
