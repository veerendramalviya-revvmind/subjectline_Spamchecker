import re
import pandas as pd
from textblob import TextBlob

# ----------------------------
# Payday Loan Keyword Lists
# ----------------------------
PAYDAY_KEYWORDS = [
    "loan", "payday", "cash", "borrow", "advance", "money", "urgent", "today",
    "fast", "quick", "instant", "approved", "credit", "bad credit", "funds",
    "deposit", "apply", "online", "same day", "get cash", "short term"
]

SPAM_TRIGGER_WORDS = [
    "free", "guaranteed", "click now", "winner", "!!!", "urgent", "act now",
    "limited", "offer", "100%", "no credit check", "instant approval"
]

# ----------------------------
# Function to analyze subject line
# ----------------------------
def analyze_subject_line(subject):
    subject_lower = subject.lower()
    
    # Keyword relevance
    keyword_hits = [kw for kw in PAYDAY_KEYWORDS if kw in subject_lower]
    relevance_score = round(len(keyword_hits) / len(PAYDAY_KEYWORDS) * 100, 2)
    
    # Spam risk
    spam_hits = [w for w in SPAM_TRIGGER_WORDS if w in subject_lower]
    spam_score = len(spam_hits) * 10  # each risky word = 10 points
    spam_score = min(spam_score, 100)
    
    # Sentiment analysis
    sentiment = TextBlob(subject).sentiment.polarity
    sentiment_label = (
        "Positive 😊" if sentiment > 0.2 else
        "Negative 😠" if sentiment < -0.2 else
        "Neutral 😐"
    )
    
    # Suggestion
    if relevance_score < 20:
        suggestion = "Add payday loan–related words like 'cash', 'loan', or 'apply today'."
    elif spam_score > 50:
        suggestion = "Too spammy — avoid excessive urgency or promises."
    elif sentiment < -0.2:
        suggestion = "Tone seems negative — make it more reassuring or helpful."
    else:
        suggestion = "Looks balanced — could perform well."
    
    return {
        "Subject": subject,
        "Relevance (%)": relevance_score,
        "Spam Risk (%)": spam_score,
        "Sentiment": sentiment_label,
        "Matched Keywords": ", ".join(keyword_hits) or "None",
        "Spam Words": ", ".join(spam_hits) or "None",
        "Suggestion": suggestion
    }

# ----------------------------
# Example Usage
# ----------------------------
subjects = [
    "Get cash instantly for your payday expenses!",
    "Apply online for quick loan approval",
    "Congratulations!!! You are a winner of free cash",
    "Protect Your Income From Costly Repair Bills!",
    "Compare 10 Best Car Insurance Companies",
    "Unlock Savings: Get Insured from $30/Month Today!"
]

results = [analyze_subject_line(sub) for sub in subjects]
df = pd.DataFrame(results)

print(df.to_string(index=False))
