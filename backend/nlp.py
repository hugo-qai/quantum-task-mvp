import spacy
from datetime import datetime, timedelta
import re

# Load small model or fallback
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

def parse_task_nlp(raw_text: str):
    """
    Simple rule-based + SpaCy NLP extraction
    """
    title = raw_text
    due_date = datetime.utcnow() + timedelta(days=1) # Default tomorrow
    smart_tags = []
    priority = 50

    # Extract tags
    smart_tags = re.findall(r"#(\w+)", raw_text)
    
    # Simple keyword heuristics for priority
    if "urgent" in raw_text.lower() or "asap" in raw_text.lower():
        priority = 90
    
    # SpaCy for entities if available (mocking useful logic for now)
    if nlp:
        doc = nlp(raw_text)
        # simplistic title cleanup
        title = doc.text

    return {
        "title": title,
        "due_date": due_date,
        "smart_tags": smart_tags,
        "predicted_priority": priority
    }

def calculate_quantum_score(task):
    """
    Score = (1/TimeUntilDue) * UserWeight + HistoricalCompletionRate
    Simplified for MVP: High priority if due soon.
    """
    if not task.due_date:
        return 0
    
    delta = (task.due_date - datetime.utcnow()).total_seconds() / 3600 # hours
    if delta <= 0:
        return 100 # Overdue
    
    score = (100 / (delta + 1)) * 10 # heuristic
    return min(int(score), 100)
