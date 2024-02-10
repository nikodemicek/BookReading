import numpy as np
import cv2
from io import BytesIO

def process_image_in_memory(in_memory_file):
    # Move the cursor to the beginning of the BytesIO buffer
    in_memory_file.seek(0)
    
    # Read the file's content into a bytes array
    file_bytes = np.asarray(bytearray(in_memory_file.read()), dtype=np.uint8)
    
    # Decode the bytes array into an OpenCV image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    return image