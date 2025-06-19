import cv2
import pytesseract
from ultralytics import YOLO
import re
from datetime import timedelta

# ✅ Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"  # Update if needed

# ✅ Load YOLO model (trained on license plates)
model = YOLO('D:/6 month/Ai Projects/smart parking system/runs/detect/train/weights/best.pt')  # Use your trained weights path

# ✅ Detect and extract plate number from image
def detect_plate_number(image):
    results = model(image)
    boxes = results[0].boxes

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_img = image[y1:y2, x1:x2]

        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(thresh, config='--psm 7')
        plate_number = re.sub(r'[^A-Z0-9]', '', text.upper())

        if len(plate_number) >= 4:
            return plate_number

    return None

def is_slot_full(vehicle_type):
    limits = {'Car': 25, 'Bike': 20, 'Bus': 5}
    from .models import PlateSession
    count = PlateSession.objects.filter(vehicle_type=vehicle_type, exit_time__isnull=True).count()
    return count >= limits.get(vehicle_type, 0)


# ✅ Vehicle type classification based on plate pattern (customizable)
def get_vehicle_type(plate_number):
    if plate_number.startswith("HP") or plate_number.startswith("DL"):
        return "Car"
    elif plate_number.startswith("PB") or plate_number.startswith("RJ"):
        return "Bike"
    elif plate_number.startswith("UP") or plate_number.startswith("HR"):
        return "Bus"
    else:
        return "Car"  # Default

# ✅ Calculate charge based on time difference
def calculate_charge(duration):
    total_minutes = duration.total_seconds() / 60
    if total_minutes <= 30:
        return 10
    elif total_minutes <= 60:
        return 20
    elif total_minutes <= 120:
        return 30
    elif total_minutes <= 180:
        return 60
    elif total_minutes <= 240:
        return 80
    elif total_minutes <= 300:
        return 100
    elif total_minutes <= 360:
        return 120
    elif total_minutes <= 420:
        return 140
    elif total_minutes <= 480:
        return 160
    elif total_minutes <= 540:
        return 180
    elif total_minutes <= 600:
        return 200
    elif total_minutes <= 660:
        return 220
    elif total_minutes <= 720:
        return 240
    else:
        return 400
