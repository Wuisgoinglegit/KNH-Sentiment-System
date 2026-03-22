import pandas as pd
import os

print("1. Loading the newly formatted datasets...")
df_swahili = pd.read_csv('swahili_data.csv', encoding='latin-1')

# This handles the English file whether it is saved as a CSV or XLSX in your folder
if os.path.exists('patient_feedback_dataset.csv'):
    df_english = pd.read_csv('patient_feedback_dataset.csv')
elif os.path.exists('patient_feedback_dataset.xlsx'):
    try:
        df_english = pd.read_excel('patient_feedback_dataset.xlsx')
    except Exception:
        df_english = pd.read_csv('patient_feedback_dataset.xlsx')
else:
    # Fallback for the exported Kaggle filename
    df_english = pd.read_csv('patient_feedback_dataset.xlsx - patient_feedback_dataset.csv')

print("2. Isolating the core columns...")
# Ensure both dataframes have the same columns before merging
df_swahili_clean = df_swahili[['Feedback', 'Sentiment']].copy()
df_english_clean = df_english[['Feedback', 'Sentiment']].copy()

print("3. Unifying the sentiment labels...")
# Converts Swahili labels like 3 - Neutral or 2 - Negative into standard text
def unify_swahili_label(label):
    label_str = str(label).lower()
    if 'positive' in label_str: return 'Positive'
    elif 'negative' in label_str: return 'Negative'
    else: return 'Neutral'

# Converts English numeric labels (1 and 0) into standard text
def unify_english_label(label):
    label_str = str(label)
    if label_str == '1': return 'Positive'
    elif label_str == '0': return 'Negative'
    else: return 'Neutral'

df_swahili_clean['Sentiment'] = df_swahili_clean['Sentiment'].apply(unify_swahili_label)
df_english_clean['Sentiment'] = df_english_clean['Sentiment'].apply(unify_english_label)

print("4. Merging into the Master Dataset...")
# Stack them together and shuffle them so the AI learns without bias
combined_df = pd.concat([df_swahili_clean, df_english_clean], ignore_index=True)
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

print("5. Saving the final AI Training Data...")
# Output the combined master CSV for the KNH sentiment engine
combined_df.to_csv('knh_training_data.csv', index=False)

print("\n=== SUCCESS ===")
print(f"Total Patient Reviews: {len(combined_df)}")
print("File successfully saved as: knh_training_data.csv")
print("\nSneak peek at your perfectly clean data:")
print(combined_df.head(5))