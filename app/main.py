from flask import  request, render_template, flash, redirect, jsonify
from flask_rq2 import RQ

from werkzeug.utils import secure_filename
import os
import logging

from app import create_app
from utils.config import allowed_file
from worker import conn
from tasks import process_image_task


logging.basicConfig(level=logging.INFO)

app = create_app()
rq = RQ(app)

from rq.job import Job
from rq import Queue
from worker import conn

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
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Enqueue the background job
            job = q.enqueue_call(func='app.tasks.process_image_task', args=(file_path,), result_ttl=5000)
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
    #port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=80)
