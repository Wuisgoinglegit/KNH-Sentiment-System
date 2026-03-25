import pickle
import re

class SentimentEngine:

    def __init__(self):
        print("Loading trained sentiment model...")

        try:
            with open("knh_sentiment_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Notice: ML Model not loaded correctly. ({e})")
            self.model = None

        # MEGA HYBRID DICTIONARY (SENTIMENT)
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

        # NEW: TRIAGE URGENCY DICTIONARY
        self.urgent_high = [
            'pain', 'uchungu', 'bleeding', 'damu', 'emergency', 'dharura', 'kufa', 
            'mahututi', 'harufu', 'wizi', 'rushwa', 'hongo', 'matusi', 'terrible', 'worst'
        ]
        
        self.urgent_medium = [
            'slow', 'waited', 'zimechelewa', 'kungoja', 'late', 'delayed', 
            'chafu', 'vichafu', 'uchafu', 'shida', 'bad', 'frustrating', 'bovu'
        ]

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text

    def contains_word(self, keyword, text):
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return re.search(pattern, text) is not None

    def predict(self, text):
        cleaned_text = self.clean_text(text)
        raw_text_lower = str(text).lower()
        
        pos_score = neg_score = neu_score = 0

        for word in self.negative_keywords:
            if self.contains_word(word, cleaned_text) or self.contains_word(word, raw_text_lower):
                neg_score += 1
        for word in self.positive_keywords:
            if self.contains_word(word, cleaned_text) or self.contains_word(word, raw_text_lower):
                pos_score += 1
        for word in self.neutral_keywords:
            if self.contains_word(word, cleaned_text) or self.contains_word(word, raw_text_lower):
                neu_score += 1

        total_score = pos_score + neg_score + neu_score
        
        if total_score > 0:
            if pos_score > 0 and pos_score == neg_score: return "Neutral"
            if neg_score > pos_score and neg_score >= neu_score: return "Negative"
            elif pos_score > neg_score and pos_score >= neu_score: return "Positive"
            else: return "Neutral"

        if self.model:
            return self.model.predict([cleaned_text])[0]
            
        return "Neutral"

    # NEW: Determines urgency weight based on risk words
    def predict_urgency(self, text, sentiment):
        # Positive feedback doesn't need urgent fixing
        if sentiment == 'Positive':
            return 'Low'
            
        raw_text_lower = str(text).lower()
        
        # 1. Check for Critical issues first (Highest weight)
        for word in self.urgent_high:
            if self.contains_word(word, raw_text_lower):
                return 'High'
                
        # 2. Check for Operational issues (Medium weight)
        for word in self.urgent_medium:
            if self.contains_word(word, raw_text_lower):
                return 'Medium'
                
        # 3. Default fallback: All other negative issues get a medium priority
        if sentiment == 'Negative':
            return 'Medium'
            
        return 'Low'