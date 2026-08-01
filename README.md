🏥 KNH — Patient Feedback Sentiment System
Intelligent Analysis Through AI & Human Oversight
Enterprise-grade Feedback Routing for Kenyatta National Hospital

| Owner | Version | Effective Date | Review Cycle |
| --- | --- | --- | --- |
| 📋 **Document Owner:** Lead Developer | 📄 **Version:** 2.0 | 📅 **Last Updated:** 2026-08-01 (EAT) | 🔄 **Review Cycle:** Quarterly |

---

### 🏆 System Deployment Excellence — ACTIVE

The KNH Sentiment System has achieved enterprise-grade operational maturity through the integration of Machine Learning classification and robust, role-based access control. Our Human-in-the-Loop (HITL) approach ensures that AI efficiency is always paired with human medical expertise.

**System Posture Summary**

| Capability | Target | Actual | Status |
| --- | --- | --- | --- |
| **Sentiment Analysis** | Real-time scoring | < 1 second | ✅ Operational |
| **Bilingual Support** | English & Swahili | 100% processing | ✅ Operational |
| **Access Control** | Strict RBAC | 6+ Department Tiers | ✅ Implemented |
| **Data Export** | PDF, Word, CSV | Live Generation | ✅ Implemented |
| **Human Oversight** | Override AI | Instant Sync | ✅ Active (v2.0) |

---

### 🤝 Why the KNH Sentiment System?

The integration of this system represents a strategic advantage for Kenyatta National Hospital's administrative and clinical workflows:

* **🏆 For Hospital Administrators:**
* **Data-Driven Decisions:** Live dashboards and charting provide an instant bird's-eye view of hospital performance.
* **Automated Triage:** Feedback is automatically routed to the correct department (e.g., Ward, Maternity, Billing) without manual sorting.


* **🏛️ For Medical Staff & QA:**
* **Human-in-the-Loop (HITL):** Clinical staff can manually review and edit AI sentiment predictions, instantly syncing the database and live charts.
* **Compartmentalized Access:** Staff only see data relevant to their specific clearance (e.g., Surgeons see Surgery/Outpatient; Pharmacists see Pharmacy).


* **💼 Business Impact:**
* Transforms raw patient feedback into actionable intelligence.
* Rapidly identifies urgent patient grievances (High Urgency tracking).



> *"True healthcare excellence comes from listening to patients at scale, and acting on their feedback with precision."*

---

### 🎯 Executive Statement

Welcome to the core repository for the KNH Sentiment System. Designed specifically for Kenyatta National Hospital, this Flask-based application leverages Scikit-learn to classify patient feedback into **Positive**, **Neutral**, or **Negative** categories.

Our system operates on a fundamental principle: AI should assist, not dictate. By implementing our new Human-in-the-Loop feature, authorized staff can override the machine learning model, ensuring that nuanced patient feedback is never misinterpreted by an algorithm.

---

### 🏛️ Quick Start for Administrators

Managing the system or conducting an audit? Start here:

**1. Staff Management (Super Admin - `ADM`)**

* Full data access across all hospital departments.
* Ability to add, delete, and manage user credentials via the secure `/manage_users` portal.

**2. Executive Review (`EXEC`, `QA`)**

* Full read-only access to all hospital data and global dashboards.

**3. Departmental Access (Clinical & Support)**

* Nurses (`NUR`) & Doctors (`DOC`): Broad access to clinical wards (Emergency, Maternity, Pediatrics, ICU, etc.).
* Specialists (`SURG`, `ONC`, `REN`): Base access plus specialty wards.
* Support (`PHARM`, `LAB`, `RAD`): Strictly compartmentalized access to their specific domains.

---

### 🚀 CI/CD & Feature Status

**Automated Document Generation**
All department analysis can be exported with a single click, dynamically generating:

* ✅ **PDF Reports:** Formatted with the KNH logo, headers, and wrapped text (`FPDF`).
* ✅ **Word Documents:** Enterprise-formatted `.docx` files (`python-docx`).
* ✅ **CSV Data:** Clean tabular data for external spreadsheet analysis.

---

### 💡 Core System Features

We've developed specialized modules that understand the KNH hospital framework and execute with minimal latency:

| Module | Domain | Key Capabilities |
| --- | --- | --- |
| 🧠 **`sentiment_engine`** | Machine Learning | Classifies English/Swahili text into Positive, Neutral, or Negative |
| 🔀 **`department_detection`** | Context Routing | Detects keywords to route feedback to the correct hospital wing |
| 🛡️ **`app.py`** | Access Control | Domain-Driven Role-Based Access Control (RBAC) & Secure Login |
| ✏️ **`HITL Override`** | Quality Assurance | Staff UI to correct AI output and adjust feedback urgency levels |
| 📊 **`Dashboard UI`** | Analytics | Dynamic Matplotlib generation, Lucide icons, responsive CSS |

---

### 📊 Repository Architecture

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

### 📅 Recent Updates

* **2026-03-26 (v2.0):** Implemented Human-in-the-Loop Override. Users can now edit AI sentiment predictions, instantly syncing the database, live charts, and all CSV/PDF/Word document exports. (Commit `193bbac`)
* **2026-03-20 (v1.5):** Implemented advanced Role-Based Access Control (RBAC) grouping logic for Executives, Front Office, Doctors, and Diagnostic staff.

---

### 📜 License & Usage

**Classification:** Confidentiality: Internal / Authorized Hospital Staff Only
This system is tailored for Kenyatta National Hospital's specific operational model. Organizations adopting this codebase should perform their own RBAC assessments and customize policies to their context.

📋 **Document Control:**

* **Distribution:** Private Repository
* **Database:** SQLite (`patient_feedback.db`)
* **Environment:** Production (Requires `.env` for mail server credentials)
