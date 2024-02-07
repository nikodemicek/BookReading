import os

import redis
from rq import Worker, Queue, Connection

from tasks import process_image_task

import sys

# Get the current file's directory
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Insert the current file's directory at the start of the PATH
sys.path.insert(0, current_file_directory)

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
