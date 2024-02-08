import os

import redis
from rq import Worker, Queue, Connection
import logging
#from tasks import process_image_task

listen = ['default']

redis_url = os.getenv('REDIS_URL')

logging.basicConfig(level=logging.INFO)


conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
