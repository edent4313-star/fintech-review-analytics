from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure lexicon is available for the test
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

def test_vader_sentiment():
    analyzer = SentimentIntensityAnalyzer()
    pos_score = analyzer.polarity_scores("I love this app, it is great!")['compound']
    neg_score = analyzer.polarity_scores("I hate this app, it is terrible.")['compound']
    assert pos_score > 0
    assert neg_score < 0

def test_thematic_mapping():
    # Simple keyword mapping test
    themes = {
        "Account Access": ["login", "account"],
        "Transaction": ["transfer", "payment"]
    }
    
    def map_theme(text):
        matched = []
        for t, keywords in themes.items():
            if any(k in text.lower() for k in keywords):
                matched.append(t)
        return matched

    assert "Account Access" in map_theme("Cannot login to my account")
    assert "Transaction" in map_theme("Payment failed")
    assert map_theme("Just a random review") == []
