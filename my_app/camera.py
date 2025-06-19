import cv2
import pytesseract
from ultralytics import YOLO
from datetime import datetime
from django.utils import timezone
from .models import PlateSession
from .utils import get_vehicle_type, calculate_charge, is_slot_full

# Set the path to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Load YOLOv8 model
model = YOLO('D:/6 month/Ai Projects/smart parking system/runs/detect/train/weights/best.pt')  # Your model path

def process_camera_feed():
    cap = cv2.VideoCapture(0)
    detected_plate = None
    start_time = datetime.now()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLOv8 detection
        results = model(frame)
        boxes = results[0].boxes

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cropped = frame[y1:y2, x1:x2]

                # Preprocessing for OCR
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 11, 17, 17)
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Tesseract OCR
                config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                text = pytesseract.image_to_string(thresh, config=config).strip()
                plate_number = ''.join(filter(str.isalnum, text)).upper()

                if plate_number and len(plate_number) >= 6:
                    print(f"✅ Plate Detected: {plate_number}")
                    detected_plate = plate_number
                    vehicle_type = get_vehicle_type(plate_number)

                    # Check if already parked (exit scenario)
                    existing = PlateSession.objects.filter(plate_number=plate_number, exit_time__isnull=True).first()
                    if existing:
                        existing.exit_time = timezone.now()
                        duration = existing.exit_time - existing.entry_time
                        existing.charge = calculate_charge(duration)
                        existing.is_paid = True  # Auto-mark as paid
                        existing.save()
                        print(f"🚪 Exit logged: {plate_number} | Time: {duration} | 💰 Charge: ₹{existing.charge}")

                    else:
                        # Entry scenario – check slot availability
                        if is_slot_full(vehicle_type):
                            print(f"❌ No slots available for {vehicle_type}")
                            cap.release()
                            cv2.destroyAllWindows()
                            return "FULL"

                        # Save entry
                        PlateSession.objects.create(
                            plate_number=plate_number,
                            vehicle_type=vehicle_type,
                            entry_time=timezone.now()
                        )
                        print(f"🚗 Entry logged: {plate_number}")

                    # Stop after successful detection
                    cap.release()
                    cv2.destroyAllWindows()
                    return plate_number

        # Show camera feed
        cv2.imshow("🔍 Scanning Vehicle Plate", frame)

        # Auto-close after 15 seconds
        if (datetime.now() - start_time).seconds > 15 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_plate






# import cv2
# import pytesseract
# from ultralytics import YOLO
# from datetime import datetime
# from django.utils import timezone
# from .models import PlateSession
# from .utils import get_vehicle_type, calculate_charge

# # Path to Tesseract (adjust if installed elsewhere)
# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# # Load YOLOv8 model
# model = YOLO('D:/6 month/Ai Projects/smart parking system/runs/detect/train/weights/best.pt')  # your model path

# def process_camera_feed():
#     cap = cv2.VideoCapture(0)
#     detected_plate = None
#     start_time = datetime.now()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)
#         boxes = results[0].boxes

#         for box in boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cropped = frame[y1:y2, x1:x2]

#             # OCR Preprocessing
#             gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
#             gray = cv2.bilateralFilter(gray, 11, 17, 17)
#             _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#             # Tesseract OCR
#             config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#             text = pytesseract.image_to_string(thresh, config=config).strip()
#             plate_number = ''.join(filter(str.isalnum, text)).upper()

#             if plate_number and len(plate_number) >= 6:
#                 print(f"✅ Plate Detected: {plate_number}")
#                 detected_plate = plate_number
#                 vehicle_type = get_vehicle_type(plate_number)

#                 # Check if entry or exit
#                 existing = PlateSession.objects.filter(plate_number=plate_number, exit_time__isnull=True).first()
#                 if existing:
#                     existing.exit_time = timezone.now()
#                     duration = existing.exit_time - existing.entry_time
#                     existing.charge = calculate_charge(duration)
#                     existing.is_paid = True  # Automatically mark as paid on exit scan
#                     existing.save()
#                     print(f"🚪 Exit logged: {plate_number} | Duration: {duration} | ✅ Marked as Paid")

#                 else:
#                     PlateSession.objects.create(
#                         plate_number=plate_number,
#                         vehicle_type=vehicle_type,
#                         entry_time=timezone.now()
#                     )
#                     print(f"🚗 Entry logged: {plate_number}")

#                 cap.release()
#                 cv2.destroyAllWindows()
#                 return plate_number

#         # Show the live detection feed
#         cv2.imshow("🔍 Scanning Vehicle Plate", frame)

#         if (datetime.now() - start_time).seconds > 15 or cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return detected_plate
