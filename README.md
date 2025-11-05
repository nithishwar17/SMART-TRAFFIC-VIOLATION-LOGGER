<<<<<<< HEAD
# 🚦 Smart Traffic Violation Logger (Flask)

## 👤 Author
**Nithishwar T**

📅 Date of Submission: November 5, 2025  
📘 College Project | Python Flask Application  

---

## 📖 Overview
The **Smart Traffic Violation Logger** is a Flask-based web application that digitalizes traffic violation management.  
It allows officers to log violations, generate QR codes, and update payment statuses.  
Citizens can scan QR codes to view their challan status — no login required.

---

## 🧩 Features
- Officer login and registration  
- Add, view, and update violations  
- Auto-generated QR codes for each record  
- Public status pages (via QR scan)  
- Secure authentication system  
- SQLite database integration  

---

## 🧱 Technologies Used
| Component | Technology |
|------------|-------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Authentication | Flask-Login, Flask-Bcrypt |
| Frontend | HTML, CSS, Bootstrap |
| QR Code | Python qrcode library |

---

## 🧭 Workflow
1. Officer logs in.
2. Adds new traffic violation.
3. Violation data is stored in the database.
4. QR code is generated for that violation.
5. Citizen scans QR to view violation status.
6. Officer can toggle between Paid / Unpaid.

---

## 🖼️ Flowchart
Below is the system flowchart:

![Flowchart](A_flowchart_in_a_digital_image_illustrates_a_smart.png)

---

## ⚙️ Setup Instructions
```bash
# Clone the repository
git clone https://github.com/nithishwar17/Smart-Traffic-Violation-Logger.git
cd Smart-Traffic-Violation-Logger

# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Linux/Mac)

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
=======
# SMART-TRAFFIC-VIOLATION-LOGGER
>>>>>>> 68b6dd9bfbb593bbaa0ed9d21c685693a8c60ec4
