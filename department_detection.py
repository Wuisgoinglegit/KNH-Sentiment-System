def detect_department(feedback):

    feedback = feedback.lower()

    departments = {
        "Emergency": ["emergency","casualty","urgent"],
        "Outpatient": ["opd","outpatient","clinic"],
        "Maternity": ["maternity","delivery","labor","midwife"],
        "Pediatrics": ["child","baby","pediatric"],
        "Pharmacy": ["pharmacy","medicine","drug"],
        "Laboratory": ["lab","blood test","sample"],
        "Radiology": ["xray","ultrasound","scan","radiology"],
        "Surgery": ["surgery","operation"],
        "Billing": ["billing","payment","bill"],
        "Reception": ["reception","front desk"],
        "Ward": ["ward","admission"]
    }

    for dept, keywords in departments.items():
        for word in keywords:
            if word in feedback:
                return dept

    return "General"