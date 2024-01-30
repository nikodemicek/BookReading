from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


from image_processor import process_image
from object_detector import detect_objects
from text_detector import detect_text_on_objects
from book_search import get_books_info, display_book_info

from utils.config import allowed_file


@app.route('/', methods=['GET', 'POST'])
def index():
    data = None 

    if request.method == 'POST':
        # handle the uploaded file
        file = request.files.get('file')
        if not file:
            flash('No file part')
            return redirect(request.url)
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Image processing steps:
            processed_image = process_image(file_path)
            detected_objects = detect_objects(processed_image, 73)
            detected_texts = detect_text_on_objects(processed_image, detected_objects)
            book_results = get_books_info(detected_texts)
            data = display_book_info(book_results, 'goodreads_avg_rating', descending=True)
        else:
            flash('Invalid file type or file too large.')
            return redirect(request.url)
        
    return render_template('index.html', data=data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
