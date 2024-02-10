from flask import  Flask, request, render_template, flash, redirect, jsonify
from flask_rq2 import RQ

from werkzeug.utils import secure_filename
import os
from io import BytesIO
import logging

from utils.config import allowed_file
from worker import conn
from tasks import process_image_task

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
rq = RQ(app)

from rq.job import Job
from rq import Queue
from worker import conn

redis_url = os.environ.get('REDIS_URL')

app.secret_key =  os.environ.get('FLASK_SECRET_KEY')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
# RQ Configuration
app.config['RQ_REDIS_URL'] = redis_url

q = Queue(connection=conn)


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
            # Use BytesIO to read the file in memory
            in_memory_file = BytesIO()
            file.save(in_memory_file)
            del file
            # Enqueue the background job
            job = q.enqueue(f=process_image_task, args=(in_memory_file,), result_ttl=5000, job_timeout=600)
            return jsonify({"job_id": job.get_id()}), 202

        else:
            flash('Invalid file type or file too large.')
            return redirect(request.url)
        
    return render_template('index.html', data=data)

@app.route('/results/<job_id>', methods=['GET'])
def get_results(job_id):
    job = Job.fetch(job_id, connection=conn)
    logging.info(f'Job status: {job.get_status()}')
    if job.is_finished:
        return jsonify(job.result), 200
    elif job.is_failed:
        return jsonify({"error": "Job failed"}), 500
    else:
        return jsonify({"status": "Processing"}), 202


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
