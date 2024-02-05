import logging
from rq.decorators import job
#from rq import Queue
#from worker import conn

from image_processor import process_image
from object_detector import detect_objects
from text_detector import detect_text_on_objects
from book_search import get_books_info, display_book_info
from app import app


#@job
def process_image_task(file_path):

    #q = Queue(connection=conn)

    # Image processing steps:
    logging.info(f'Processing image: {file_path}')
    processed_image = process_image(file_path)
    logging.info(f'Image processed')
    detected_objects = detect_objects(processed_image, 73)
    logging.info(f'Objects detected')
    detected_texts = detect_text_on_objects(processed_image, detected_objects)
    logging.info(f'Texts detected')
    book_results = get_books_info(detected_texts)
    logging.info(f'Books info retrieved')
    return display_book_info(book_results, 'goodreads_avg_rating', descending=True)