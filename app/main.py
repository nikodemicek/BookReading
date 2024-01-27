from ui import get_user_input, display_results
from image_processor import process_image
from object_detector import detect_objects
from text_detector import detect_text_on_objects
from book_search import get_book_info, display_book_info
#from data_formatter import format_data_for_display

def main():
    # Step 1: UI to accept a picture
    image_path = get_user_input()

    # Step 2: Process the image (if necessary)
    processed_image = process_image(image_path)

    # Step 3: Detect objects in the picture (73 is an object class 'book' in the COCO dataset)
    detected_objects = detect_objects(processed_image, 73)

    # Step 4: Detect text on each object
    detected_texts = detect_text_on_objects(processed_image, detected_objects)
    print(f"Number of books detected: {len(detected_texts)}")

    # Step 5: Search the detected text using an API
    book_results = [get_book_info(text) for text in detected_texts]

    # Step 6: Format the data for UI presentation
    formatted_data = display_book_info(book_results, 'goodreads_avg_rating', descending=True)

    # Displaying the results in the UI
    display_results(formatted_data)

if __name__ == "__main__":
    main()
