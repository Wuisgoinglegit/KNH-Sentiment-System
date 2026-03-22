import pandas as pd
import pickle
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# TEXT CLEANING FUNCTION
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

print("1. Loading merged dataset...")

data = pd.read_csv("knh_training_data.csv")

# Remove empty feedback
data = data.dropna(subset=["Feedback"])

# Clean text
data["Feedback"] = data["Feedback"].apply(clean_text)

print("2. Separating features and labels...")

X = data["Feedback"]
y = data["Sentiment"]

print("3. Splitting dataset into training and testing sets...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("4. Building ML pipeline (TF-IDF + Logistic Regression)...")

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1,3),   # or (1,3) for better performance
        stop_words="english"
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

print("5. Training the classifier...")

model.fit(X_train, y_train)

print("6. Testing the model...")

predictions = model.predict(X_test)

print("\nModel Accuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("7. Saving the trained model...")

with open("knh_sentiment_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\n=== TRAINING COMPLETE ===")
print("Model saved as: knh_sentiment_model.pkl")