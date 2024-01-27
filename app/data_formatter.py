from ui import get_user_input, display_results
from image_processor import process_image
from object_detector import detect_objects
from text_detector import detect_text_on_objects
from api_searcher import search_api
from data_formatter import format_data_for_display

def main():
    # Step 1: UI to accept a picture
    image_path = get_user_input()

    # Step 2: Process the image (if necessary)
    processed_image = process_image(image_path)

    # Step 3: Detect objects in the picture
    detected_objects = detect_objects(processed_image)

    # Step 4: Detect text on each object
    detected_texts = detect_text_on_objects(detected_objects)

    # Step 5: Search the detected text using an API
    search_results = [search_api(text) for text in detected_texts]

    # Step 6: Format the data for UI presentation
    formatted_data = format_data_for_display(detected_objects, search_results)

    # Displaying the results in the UI
    display_results(formatted_data)

if __name__ == "__main__":
    main()
