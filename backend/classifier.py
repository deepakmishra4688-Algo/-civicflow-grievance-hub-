from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from backend.training_data import get_training_data

# Get large training dataset (500+ samples)
all_texts, all_labels = get_training_data()

# Initialize classifier
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', max_features=1000)
classifier = MultinomialNB()

# Train on large dataset
X_train = vectorizer.fit_transform(all_texts)
classifier.fit(X_train, all_labels)

priority_keywords = ['urgent', 'emergency', 'critical', 'danger', 'accident', 'flood', 'collapse', 'unsafe', 'accident']

def classify_complaint(text):
    """Classify complaint text into category and priority"""
    if not text or len(text.strip()) == 0:
        return {
            'category': 'Public Services',
            'department': 'Public Services Office',
            'priority': 'Normal'
        }
    
    # Transform text and predict category
    text_vector = vectorizer.transform([text.lower()])
    category = classifier.predict(text_vector)[0]
    
    # Determine department
    department_map = {
        'Electricity': 'Electrical Services',
        'Water Supply': 'Water Department',
        'Sanitation': 'Sanitation & Waste Management',
        'Roads': 'Roads & Transport',
        'Public Services': 'Public Services Office'
    }
    department = department_map.get(category, 'Public Services Office')
    
    # Determine priority
    text_lower = text.lower()
    priority = 'High' if any(keyword in text_lower for keyword in priority_keywords) else 'Normal'
    
    # Boost priority for longer complaints
    if len(text) > 200:
        priority = 'High' if priority == 'High' else 'Medium'
    
    return {
        'category': category,
        'department': department,
        'priority': priority
    }
