from src.thematic_analysis import get_primary_theme, assign_themes, top_themes_by_bank


def test_get_primary_theme_account_access():
    assert get_primary_theme("I cannot login to my account") == "Account Access"
    assert get_primary_theme("Password reset is broken") == "Account Access"


def test_get_primary_theme_transaction():
    assert get_primary_theme("Transfer failed during payment") == "Transaction"
    assert get_primary_theme("I cannot send money") == "Transaction"


def test_assign_themes_returns_theme_list():
    reviews = [
        "Login page is broken",
        "App crashes and freezes",
    ]
    themes = assign_themes(reviews)
    assert themes[0] == "Account Access"
    assert themes[1] == "Stability & Performance"


def test_top_themes_by_bank_returns_bank_summary():
    import pandas as pd

    df = pd.DataFrame([
        {"bank_name": "BankA", "identified_theme": "Transaction", "sentiment_score": 0.8},
        {"bank_name": "BankA", "identified_theme": "Account Access", "sentiment_score": -0.2},
        {"bank_name": "BankB", "identified_theme": "Usability & UX", "sentiment_score": 0.6},
    ])
    summary = top_themes_by_bank(df, bank_col="bank_name", theme_col="identified_theme", sentiment_col="sentiment_score", top_n=1)
    assert summary["BankA"]["positive_themes"] == {"Transaction": 0.8}
    assert summary["BankA"]["negative_themes"] == {"Account Access": -0.2}
    assert summary["BankB"]["positive_themes"] == {"Usability & UX": 0.6}
