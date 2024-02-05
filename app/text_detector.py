import re 

import pytesseract


def extract_text_and_numbers_with_spaces(text):
    return ' '.join(re.findall(r'[a-zA-Z0-9]+', text))

def read_book_text(image, book_box):
    x1, y1, x2, y2 = map(int, book_box)
    roi = image[y1:y2, x1:x2]
    """
    # Determine if the ROI is vertically oriented - IMPROVE THIS!!!!!!!
    height, width = roi.shape[:2]
    spine_facing = height / width > 4
    if spine_facing:
        roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
    """
    # Use pytesseract to read text from the ROI
    text = pytesseract.image_to_string(roi, config='--psm 5')
    return text

def detect_text_on_objects(processed_image, detected_objects):
    """
    Detects text on each object in the image.
    :param processed_image: The image to be processed.
    :param detected_objects: The objects detected in the image.
    :return: A list of the text detected on each object.
    """
    # Loop through each detected book
    list_of_books = []
    for i, box in enumerate(detected_objects):
        list_of_books.append(extract_text_and_numbers_with_spaces(read_book_text(processed_image, box)))
    
    return list_of_books

