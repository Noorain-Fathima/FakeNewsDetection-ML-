import pandas as pd
import re
import pickle

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
news_dataset = pd.read_csv("train.csv", encoding="ISO-8859-1")
news_dataset = news_dataset.fillna('')

# Combine title and text
news_dataset['content'] = news_dataset['title'] + " " + news_dataset['text']

# Preprocessing
port_stem = PorterStemmer()
stop_words = set(stopwords.words('english'))

def stemming(content):
    content = re.sub('[^a-zA-Z]', ' ', content)
    content = content.lower()
    content = content.split()
    content = [port_stem.stem(word) for word in content if word not in stop_words]
    return ' '.join(content)

news_dataset['content'] = news_dataset['content'].apply(stemming)

X = news_dataset['content']
Y = news_dataset['label']

# TFIDF
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=0.7)
X = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X, Y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully!")