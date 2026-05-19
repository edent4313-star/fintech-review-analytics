import pytest
import pandas as pd
from src.data_scraper import scrape_fintech_reviews

def test_scrape_fintech_reviews_structure():
    """
    Tests that the scraper returns a correctly structured DataFrame.
    We use a count of 1 to keep the test fast.
    """
    test_apps = {'TestApp': 'com.paypal.android.p2pmobile'}
    df = scrape_fintech_reviews(test_apps, count=1)
    
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'app' in df.columns
        assert 'review' in df.columns
        assert 'rating' in df.columns
