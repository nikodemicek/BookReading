import logging


from image_processor import process_image_in_memory
from object_detector import detect_objects
from text_detector import detect_text_on_objects
from book_search import get_books_info, display_book_info


def process_image_task(in_memory_file):

    # Image processing steps:
    logging.info(f'Lets go! Processing image: {in_memory_file.name}')
    processed_image = process_image_in_memory(in_memory_file)
    logging.info(f'Image processed')
    detected_objects = detect_objects(processed_image, 73)
    logging.info(f'Objects detected')
    detected_texts = detect_text_on_objects(processed_image, detected_objects)
    logging.info(f'Texts detected')
    book_results = get_books_info(detected_texts)
    logging.info(f'Books info retrieved')
    final_results = display_book_info(book_results, 'goodreads_avg_rating', descending=True)
    return final_results