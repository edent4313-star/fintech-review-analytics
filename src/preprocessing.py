import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import os

# ============================================================================
# NLTK DATA SETUP - Runs on module import to ensure data is available
# ============================================================================
def _ensure_nltk_data():
    """Download NLTK data if not already present."""
    nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
    
    # Add to path if not already there
    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.insert(0, nltk_data_dir)
    
    # Define required resources
    resources_to_check = {
        'stopwords': 'corpora/stopwords',
        'wordnet': 'corpora/wordnet',
        'punkt': 'tokenizers/punkt',
        'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger'
    }
    
    for resource_name, resource_path in resources_to_check.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                nltk.download(resource_name, quiet=True, download_dir=nltk_data_dir)
            except Exception as e:
                print(f"Warning: Could not download {resource_name}: {e}")

# Run on import
_ensure_nltk_data()

# ============================================================================
# PREPROCESSING FUNCTIONS
# ============================================================================

def clean_text(text):
  
    if not isinstance(text, str):
        if pd.isna(text):
            return ""
        text = str(text) # Force string conversion for numeric data
    
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\d+", "", text)
    return text

def tokenize_and_lemmatize(text):
    """
    Tokenizes text, removes stopwords, and applies lemmatization.
    Matches the notebook's modular_nlp_pipeline logic.
    """
    # 1. Cleaning (Regex)
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text).lower())

    # 2. Tokenization
    tokens = nltk.word_tokenize(text)

    # 3. Stop-word removal & Lemmatization
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    return " ".join(processed)

def preprocess_dataframe(df, text_column='review'):
    """
    Applies the full preprocessing pipeline to a dataframe.
    ERROR HANDLING: Row-level exception handling to prevent pipeline crashes.
    """
    try:
        df['clean_text'] = df[text_column].apply(clean_text)
        df['processed_content'] = df['clean_text'].apply(tokenize_and_lemmatize)
        return df
    except Exception as e:
        print(f" ERROR: Preprocessing failed on column '{text_column}': {e}")
        return df

def robust_clean(df):
    """
     ERROR HANDLING: Data Integrity Checks
    Handles schema validation, type enforcement, and date normalization.
    """
    try:
        # 1. Strip Whitespaces & Trailing Zeros
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.replace(r'\.0$', '', regex=True)

        # 2. Date Normalisation
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # 3. Handle Missing Values
        print(f"Nulls before: {df.isnull().sum().sum()}")
        df = df.dropna(subset=['review', 'rating'])

        # 4. Filter empty/short reviews
        df = df[df['review'].str.len() > 2]

        print(f"Final Nulls: {df.isnull().sum().sum()}")
        print(f"Final Dataset Shape: {df.shape}")
        return df.reset_index(drop=True)
    except Exception as e:
        print(f" ERROR: Robust cleaning failed: {e}")
        return df
