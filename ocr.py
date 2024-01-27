import cv2
import pytesseract

# Specify the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\NikodemOlsavsky\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"


def read_book_text(image, book_box):
    x1, y1, x2, y2 = map(int, book_box)
    roi = image[y1:y2, x1:x2]

    # Determine if the ROI is vertically oriented - IMPROVE THIS!!!!!!!
    height, width = roi.shape[:2]
    spine_facing = height / width > 4
    if spine_facing:
        roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    # Use pytesseract to read text from the ROI
    text = pytesseract.image_to_string(roi, config='--psm 3')
    return text