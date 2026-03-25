import pickle
import re

class SentimentEngine:

    def __init__(self):
        print("Loading trained sentiment model...")

        # Loading the trained model
        try:
            with open("knh_sentiment_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Notice: ML Model not loaded correctly. ({e})")
            self.model = None

        # MEGA HYBRID DICTIONARY
        self.negative_keywords = [
            'zimechelewa', 'vichafu', 'ndefu', 'shida', 'mbaya', 'vibaya', 'uchungu', 
            'kungoja', 'kuzubaa', 'hakuna', 'bovu', 'chafu', 'harufu', 'kelele', 
            'wizi', 'hongo', 'rushwa', 'maringo', 'madharau', 'bure', 'matusi', 'kujivuna',
            'kuchelewa', 'mbovu', 'uchafu', 'maji hayako', 'useless',
            'slow', 'frustrating', 'waited', 'not working', 'bad', 'terrible', 
            'horrible', 'rude', 'dirty', 'unprofessional', 'ignored', 'pain', 
            'late', 'unhelpful', 'worse', 'worst', 'challenge', 'delayed'
        ]
        
        self.positive_keywords = [
            'safi', 'mzuri', 'bora', 'vizuri', 'namshukuru', 'asante', 'shukrani', 
            'barikiwa', 'chapchap', 'haraka', 'poa', 'fiti', 'bomba', 'kusaidia', 
            'roho safi', 'karimu', 'kujali', 'mubarikiwe',
            'top notch', 'fast', 'helpful', 'kind', 'safe', 'professionally', 
            'big up', 'went well', 'good', 'excellent', 'amazing', 'great', 
            'caring', 'clean', 'quick', 'fantastic', 'loved', 'best'
        ]
        
        self.neutral_keywords = [
            'okay', 'routine', 'lakini mwishowe', 'bili', 'normal', 'checkup',
            'just waiting', 'average', 'fine', 'sawa', 'kawaida'
        ]

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

        # Step 2: Scoring System
        raw_text_lower = str(text).lower()
        
        pos_score = 0
        neg_score = 0
        neu_score = 0

        # Tally Negative points
        for word in self.negative_keywords:
            if word in cleaned_text or word in raw_text_lower:
                neg_score += 1

        # Tally Positive points
        for word in self.positive_keywords:
            if word in cleaned_text or word in raw_text_lower:
                pos_score += 1

        # Tally Neutral points
        for word in self.neutral_keywords:
            if word in cleaned_text or word in raw_text_lower:
                neu_score += 1

        # Evaluate Hybrid Scores if any keywords were found
        total_score = pos_score + neg_score + neu_score
        
        if total_score > 0:
            print(f"HYBRID SCORES -> Pos: {pos_score}, Neg: {neg_score}, Neu: {neu_score}")
            
            # Tiebreaker: If it has equal good and bad things, it's mixed (Neutral)
            if pos_score > 0 and pos_score == neg_score:
                print("HYBRID RESULT: Neutral (Mixed feedback)")
                return "Neutral"
                
            # Highest score wins
            if neg_score > pos_score and neg_score >= neu_score:
                print("HYBRID RESULT: Negative")
                return "Negative"
            elif pos_score > neg_score and pos_score >= neu_score:
                print("HYBRID RESULT: Positive")
                return "Positive"
            else:
                print("HYBRID RESULT: Neutral")
                return "Neutral"

        # Step 3: Predict using the trained model (If no dictionary words were found)
        if self.model:
            prediction = self.model.predict([cleaned_text])[0]
            print(f"Model Prediction: {prediction}")
            return prediction
            
        return "Neutral" # Ultimate fallback