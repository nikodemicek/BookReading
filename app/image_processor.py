import numpy as np
import os
import cv2
import boto3
import logging

def process_image_in_memory(file_key, bucket_name):
    """
    Fetch an image from S3 and process it in memory.
    """
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    #BUCKET_NAME = os.environ.get("BUCKET_NAME")

    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Fetch the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    image_content = response['Body'].read()

    # Convert the image data to a numpy array
    image_array = np.asarray(bytearray(image_content), dtype=np.uint8)

    # Use OpenCV to read the image data
    image = cv2.imdecode(image_array, -1)  # The '-1' flag tells OpenCV to read the image as is (including alpha channel if present)
    
    return image