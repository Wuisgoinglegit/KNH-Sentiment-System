import pickle
import re

class SentimentEngine:

    def __init__(self):
        print("Loading trained sentiment model...")

        # Loading the trained model
        with open("knh_sentiment_model.pkl", "rb") as f:
            self.model = pickle.load(f)

        print("Model loaded successfully!")

    # SAME cleaning used during training
    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text

    def predict(self, text):

        print("\n--- NEW REVIEW INCOMING ---")
        print(f"Original Text: {text}")

        # Step 1: Clean text
        cleaned_text = self.clean_text(text)
        print(f"Cleaned Text: {cleaned_text}")

        # Step 2: Predict using the trained model
        prediction = self.model.predict([cleaned_text])[0]
        print(f"Model Prediction: {prediction}")

        return prediction