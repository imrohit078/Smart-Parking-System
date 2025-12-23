 Smart Parking Management System (Django + YOLOv8)
A smart web-based parking system built with Django, YOLOv8, and Tesseract OCR, allowing employees to manage vehicle entries/exits, detect number plates and calculate charges based on parking duration.

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

🔐 Roles
Admin: Can access Django admin, manage all sessions
Employee:Login and see restricted dashboard Add/edit vehicle sessions (entry, exit, charges, slot)
Detect plates or manually enter them

💰 Charges Logic
Auto-calculated as:
charge = base_rate + (duration in hours × hourly_rate)
Employee can override with custom charge

