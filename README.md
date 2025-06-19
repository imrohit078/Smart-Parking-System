 Smart Parking Management System (Django + YOLOv8)
A smart web-based parking system built with Django, YOLOv8, and Tesseract OCR, allowing employees to manage vehicle entries/exits, detect number plates, assign dynamic parking slots (like A1, B2), and calculate charges based on parking duration.

📌 Features
🔐 Employee login system

🅿️ Vehicle slot allocation (A1, B2... based on vehicle type)

📸 Live webcam detection for number plates (YOLOv8 + Tesseract)

✍️ Manual vehicle entry option for employees

🧾 Parking charge calculation based on time or custom entry

📤 Downloadable PDF receipts

📊 Earnings report

📁 Media folder support for saving plate captures

🎨 Responsive UI using Bootstrap 5

💻 Technologies Used
Backend: Django 5+

Frontend: HTML, Bootstrap 5, JavaScript

Detection: YOLOv8 (Ultralytics), Tesseract OCR

Database: MySQL / SQLite

Camera Handling: OpenCV

🗂️ Project Structure
csharp
Copy
Edit
smart_parking/
│
├── parking_app/
│   ├── models.py          # PlateSession, ParkingSlot, EmployeeProfile
│   ├── views.py           # Detection, manual entry, slot logic
│   ├── forms.py           # Manual + Update session forms
│   ├── urls.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── manual_entry.html
│   │   ├── update_session.html
│
├── media/
│   └── results/           # Detected plate images
│
├── camera.py              # YOLOv8 & Tesseract integrated detection
├── utils.py               # Charge calculation, slot check functions
├── requirements.txt
└── manage.py
🧠 YOLOv8 + Tesseract OCR
Detects vehicle number plate using YOLOv8

Extracts text via pytesseract from cropped ROI

Returns plate number to Django view to store in database

🛠️ Setup Instructions
Clone the Repo

bash
Copy
Edit
git clone https://github.com/yourusername/smart-parking-system.git
cd smart-parking-system
Create & Activate Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Requirements

bash
Copy
Edit
pip install -r requirements.txt
Set up Database

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Create Superuser

bash
Copy
Edit
python manage.py createsuperuser
Run Server

bash
Copy
Edit
python manage.py runserver
📷 YOLOv8 Detection
Trained YOLOv8 model on license plate dataset

Stores detected plate in database if entry is valid

Detection only runs for 15 seconds per session (configurable)

🔐 Roles
Admin: Can access Django admin, manage all sessions

Employee:

Login and see restricted dashboard

Add/edit vehicle sessions (entry, exit, charges, slot)

Detect plates or manually enter them

💰 Charges Logic
Auto-calculated as:
charge = base_rate + (duration in hours × hourly_rate)

Employee can override with custom charge

