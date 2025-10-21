# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for Detectron2 and Tesseract
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install torch==2.1.0+cpu torchvision==0.16.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

# Copy your application files to the container
COPY ./app .

# download the Detectron2 model weights
RUN python object_detector.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME dockerenv

# Run app.py when the container launches
CMD ["python", "main.py"]
