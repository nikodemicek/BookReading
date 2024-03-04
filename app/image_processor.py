import numpy as np
import os
import cv2
import boto3
from io import BytesIO

def process_image_in_memory(file_key):

    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    
    # Create a BytesIO object to hold the file data
    file_obj = BytesIO()
    
    # Download file from S3 into the BytesIO object
    s3.download_fileobj(Bucket=BUCKET_NAME, Key=file_key, Fileobj=file_obj)
    
    # Move the cursor to the beginning of the BytesIO object
    file_obj.seek(0)
    
    # Read the file's content into a bytes array
    file_bytes = np.asarray(bytearray(file_obj.read()), dtype=np.uint8)
    
    # Decode the bytes array into an OpenCV image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    return image