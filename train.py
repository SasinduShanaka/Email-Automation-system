import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load dataset
df = pd.read_csv("data/emails.csv")

X = df["text"]
y = df["label"]

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Build ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

# 4. Train model
model.fit(X_train, y_train)

# 5. Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. Save model
with open("models/email_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully")
