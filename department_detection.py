def detect_department(feedback):
    """
    Analyzes feedback text to identify relevant hospital departments 
    using Standard English and Swahili keywords.
    """
    feedback = feedback.lower()

    # Bilingual Mapping: English Key - List of English and Swahili Keywords
    departments = {
        "Emergency": ["emergency", "casualty", "urgent", "ajali", "haraka", "triage"],
        "Outpatient": ["opd", "outpatient", "clinic", "kliniki", "mapokezi"],
        "Maternity": ["maternity", "delivery", "labor", "midwife", "uzazi", "kujifungua"],
        "Pediatrics": ["child", "baby", "pediatric", "watoto", "mtoto"],
        "Pharmacy": ["pharmacy", "medicine", "drug", "dawa", "chemist"],
        "Laboratory": ["lab", "blood test", "sample", "maabara", "vipimo", "damu"],
        "Radiology": ["xray", "ultrasound", "scan", "picha", "mionzi"],
        "Surgery": ["surgery", "operation", "upasuji", "thiyeta"],
        "Billing": ["billing", "payment", "bill", "malipo", "pesa", "kaunta"],
        "Reception": ["reception", "front desk", "huduma kwa wateja"],
        "Ward": ["ward", "admission", "kulazwa", "wodini"]
    }

    found_depts = []

    # Run through again the dictionary to find all matches
    for dept, keywords in departments.items():
        for word in keywords:
            # Check for the word with spaces to avoid partial matches (like 'lab' in 'label')
            if f" {word} " in f" {feedback} ":
                if dept not in found_depts:
                    found_depts.append(dept)
                break 

    # Return a comma-separated string of departments, or "General" if none found
    if found_depts:
        return ", ".join(found_depts)
    
    return "General"