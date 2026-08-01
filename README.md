# 🏥 KNH — Patient Feedback Sentiment System
Intelligent Analysis Through AI & Human Oversight
Proof-of-Concept Feedback Routing for Kenyatta National Hospital

| Owner | Version | Effective Date | Project Type |
| :--- | :--- | :--- | :--- |
| 📋 **Document Owner:** Wuisgoinglegit | 📄 **Version:** 2.0 | 📅 **Last Updated:** 2026-08-01 (EAT) | 🎓 **Type:** Institution Semester Project |

---

## 🎓 Academic Project Status
The KNH Sentiment System is a personalospit semester project designed as a proof-of-concept. Rather than being deployed and tested in live hospital environments, the system is an actively evolving technical demonstration. I am incrementally expanding the system by adding new department categories and refining the dynamic routing logic over time to showcase how such a platform could scale. By prioritizing a Human-in-the-Loop (HITL) approach early on, this project demonstrates how AI efficiency can be safely paired with human medical expertise.

**Current System Capabilities**

| Capability | Target | Actual | Status |
| :--- | :--- | :--- | :--- |
| **Sentiment Analysis** | Real-time scoring | < 1 second | ✅ Operational |
| **Bilingual Support** | English & Swahili | 100% processing | ✅ Operational |
| **Access Control** | Strict RBAC | Simulated Departments | 🔄 Expanding |
| **Data Export** | PDF, Word, CSV | Live Generation | ✅ Implemented |
| **Human Oversight** | Override AI | Instant Sync | ✅ Active (v2.0) |

---

## 🤝 Project Objectives & Conceptual Benefits
This project explores how integrating a machine learning sentiment system could theoretically provide a strategic advantage for Kenyatta National Hospital's administrative and clinical workflows:

*   **🏆 For Hospital Administrators (Concept):**
    *   **Data-Driven Decisions:** Live dashboards and charting to provide an instant bird's-eye view of hospital performance.
    *   **Automated Triage:** Feedback automatically routed to the correct conceptual department (e.g., Ward, Maternity, Billing) without manual sorting.
*   **😷 For Medical Staff & QA (Concept):**
    *   **Human-in-the-Loop (HITL):** Clinical staff can manually review and edit AI sentiment predictions, instantly syncing the database and live charts.
    *   **Compartmentalized Access:** Simulating a scenario where staff only see data relevant to their specific clearance.
*   **💼 System Impact:**
    *   Demonstrates the transformation of raw patient feedback into actionable intelligence.
    *   Explores tracking mechanisms for highly urgent patient grievances.

> *"Exploring healthcare excellence through simulated patient listening at scale and precision feedback routing."*

---

## 🎯 Executive Statement
Welcome to the core repository for the KNH Sentiment System. Designed as a semester project simulating workflows for Kenyatta National Hospital, this Flask-based application leverages Scikit-learn to classify patient feedback into **Positive**, **Neutral**, or **Negative** categories. 

This system operates on a fundamental principle: AI should assist, not dictate. By implementing a Human-in-the-Loop feature, the project demonstrates how authorized users could override a machine learning model, ensuring that nuanced feedback is never misinterpreted by an algorithm. 

---

## ⚕️ System Demonstration (Access Control)
To demonstrate Role-Based Access Control (RBAC), the project features simulated clearance levels:

**1. Staff Management (Super Admin - `ADM`)**
*   Full data access across all simulated hospital departments.
*   Ability to add, delete, and manage user credentials via the secure `/manage_users` portal.

**2. Executive Review (`EXEC`, `QA`)**
*   Full read-only access to all hospital data and global dashboards.

**3. Departmental Access (Clinical & Support)**
*   Nurses (`NUR`) & Doctors (`DOC`): Broad access to simulated clinical wards.
*   Specialists (`SURG`, `ONC`, `REN`): Base access plus specialty wards.
*   Support (`PHARM`, `LAB`, `RAD`): Strictly compartmentalized access to specific simulated domains.

---

## 🚀 CI/CD & Feature Status

**Automated Document Generation**
All department analysis can be exported with a single click, dynamically generating:
*   ✅ **PDF Reports:** Formatted with the KNH logo, headers, and wrapped text (`FPDF`).
*   ✅ **Word Documents:** Enterprise-formatted `.docx` files (`python-docx`).
*   ✅ **CSV Data:** Clean tabular data for external spreadsheet analysis.

---

## 💡 Core System Features
I have developed specialized modules that understand the theoretical KNH hospital framework and execute with minimal latency:

| Module | Domain | Key Capabilities |
| :--- | :--- | :--- |
| 🧠 **`sentiment_engine`** | Machine Learning | Classifies English/Swahili text into Positive, Neutral, or Negative |
| 🔀 **`department_detection`** | Context Routing | Detects keywords to dynamically route feedback |
| 🛡️ **`app.py`** | Access Control | Domain-Driven Role-Based Access Control (RBAC) & Secure Login |
| ✏️ **`HITL Override`** | Quality Assurance | UI to correct AI output and adjust feedback urgency levels |
| 📊 **`Dashboard UI`** | Analytics | Dynamic Matplotlib generation, Lucide icons, responsive CSS |

---

## 📊 Repository Architecture

```text
KNH-Sentiment-System/
├── ⚙️ app.py                      # Main Flask application & RBAC logic
├── 🧠 sentiment_engine.py         # AI sentiment classification logic
├── 🔀 department_detection.py     # Dynamic feedback routing
├── 🛠️ train_model.py              # ML training scripts
├── 📂 static/                     # KNH logos, CSS, and UI assets
├── 📂 templates/                  # Frontend HTML
│   ├── dashboard.html             # Global hospital view
│   ├── analysis.html              # Department-specific view
│   ├── login.html                 # Secure authentication portal
│   └── manage_users.html          # Super Admin dashboard
└── 🗄️ Datasets                    # knh_training_data.csv, swahili_data.csv

```

---

## 📅 Recent Updates

* **2026-03-26 (v2.0):** Implemented Human-in-the-Loop Override. Users can now edit AI sentiment predictions, instantly syncing the database, live charts, and all CSV/PDF/Word document exports. (Commit `193bbac`)
* **2026-03-20 (v1.5):** Implemented advanced Role-Based Access Control (RBAC) grouping logic to simulate Executives, Front Office, Doctors, and Diagnostic staff access.

---

## 📜 License & Usage

**Classification:** Academic Proof-of-Concept
This system is a personal academic project modeled around Kenyatta National Hospital's operational structure. It is not currently deployed in a real-world medical environment.

📋 **Document Control:**

* **Distribution:** Public/Private Repository
* **Database:** SQLite (`patient_feedback.db`)
* **Environment:** Development/Local (Requires `.env` for mail server credentials)

```

```
