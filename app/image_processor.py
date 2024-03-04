import numpy as np
import os
import cv2
import boto3
from io import BytesIO

def process_image_in_memory(file_key):

    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    
    # Fetch the image from S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    image_content = response['Body'].read()

    # Convert the image data to a numpy array
    image_array = np.asarray(bytearray(image_content), dtype=np.uint8)

    # Use OpenCV to read the image data
    image = cv2.imdecode(image_array, -1)  # The '-1' flag tells OpenCV to read the image as is (including alpha channel if present)
    
    return image