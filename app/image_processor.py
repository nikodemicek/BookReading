import cv2

def process_image(image_path):
    print(f"Processing image at {image_path}")
    image = cv2.imread(image_path)
    return image
