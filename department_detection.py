def detect_department(feedback):
    # Standardizing text to lowercase
    text = feedback.lower()

    # Expanded Bilingual Mapping for KNH Specialized Units
    departments = {
        "Emergency": ["emergency", "casualty", "urgent", "ajali", "haraka", "triage"],
        "Outpatient": ["opd", "outpatient", "clinic", "kliniki", "mapokezi"],
        "Maternity": ["maternity", "delivery", "labor", "midwife", "uzazi", "kujifungua"],
        "Pediatrics": ["child", "baby", "pediatric", "watoto", "mtoto"],
        "Pharmacy": ["pharmacy", "medicine", "drug", "dawa", "chemist"],
        "Laboratory": ["lab", "blood test", "sample", "maabara", "vipimo", "damu"],
        "Radiology": ["xray", "ultrasound", "scan", "picha", "mionzi"],
        "Surgery": ["surgery", "operation", "upasuji", "theatre"],
        "Billing": ["billing", "payment", "bill", "malipo", "pesa", "kaunta"],
        "Reception": ["reception", "front desk", "huduma kwa wateja"],
        "Ward": ["ward", "admission", "kulazwa", "wodini"],
        "ICU": ["icu", "hdu", "critical care", "mahututi", "isolation"],
        "Renal": ["renal", "dialysis", "kidney", "figo", "kusafisha damu"],
        "Dental": ["dental", "tooth", "teeth", "meno", "kung'oa", "dentist"],
        "Oncology": ["cancer", "oncology", "chemotherapy", "kansa", "saratani", "clinic 13"]
    }

    found_depts = []

    # Looping through the units and checking keywords
    for dept, keywords in departments.items():
        for word in keywords:
            # Using the space trick to ensure whole words are only matched
            if f" {word} " in f" {text} ":
                if dept not in found_depts:
                    found_depts.append(dept)
                break 

    # Return matches or fallback to General
    if found_depts:
        return ", ".join(found_depts)
    
    return "General"