from ultralytics import YOLO
import numpy as np

def get_model_weights(model_size='m'):
    """
    Initialize YOLO model.
    
    Parameters
    ----------
    model_size : str
        Model size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (xlarge)
        Larger = more accurate but slower
    
    Returns
    -------
    model : YOLO
        The initialized YOLO model
    """
    # Load pretrained model (will auto-download on first use)
    model = YOLO(f'yolov8{model_size}.pt')
    return model

# Initialize model
model = get_model_weights('m')  # Medium model - good balance

def detect_objects(image, object_class='book', confidence_threshold=0.5):
    """
    Detects objects in an image.

    Parameters
    ----------
    image : numpy.ndarray or str
        The image to process (numpy array or path to image file).
    object_class : str or int
        The class name (e.g., 'book') or COCO class ID (e.g., 84 for books)
    confidence_threshold : float
        Minimum confidence score for detections (0-1)

    Returns
    -------
    object_boxes : numpy.ndarray
        The bounding boxes of the detected objects in format [x1, y1, x2, y2]
    """
    # Make prediction
    results = model(image, conf=confidence_threshold, verbose=False)
    
    # Get the first result (single image)
    result = results[0]
    
    # COCO dataset class ID for 'book' is 84
    if isinstance(object_class, str):
        if object_class.lower() == 'book':
            object_class = 84
        else:
            # Try to find class by name
            class_names = result.names
            object_class = next((k for k, v in class_names.items() if v.lower() == object_class.lower()), None)
            if object_class is None:
                return np.array([])
    
    # Filter detections by class
    boxes = result.boxes
    class_ids = boxes.cls.cpu().numpy()
    object_indices = np.where(class_ids == object_class)[0]
    
    if len(object_indices) == 0:
        return np.array([])
    
    # Get bounding boxes for the specified class
    object_boxes = boxes.xyxy.cpu().numpy()[object_indices]
    
    return object_boxes


def detect_objects_with_details(image, object_class='book', confidence_threshold=0.5):
    """
    Detects objects and returns detailed information.

    Parameters
    ----------
    image : numpy.ndarray or str
        The image to process.
    object_class : str or int
        The class name or COCO class ID
    confidence_threshold : float
        Minimum confidence score for detections

    Returns
    -------
    detections : list of dict
        List of detections with boxes, confidence scores, and class info
    """
    results = model(image, conf=confidence_threshold, verbose=False)
    result = results[0]
    
    # Convert class name to ID if needed
    if isinstance(object_class, str):
        if object_class.lower() == 'book':
            object_class = 84
        else:
            class_names = result.names
            object_class = next((k for k, v in class_names.items() if v.lower() == object_class.lower()), None)
            if object_class is None:
                return []
    
    boxes = result.boxes
    class_ids = boxes.cls.cpu().numpy()
    confidences = boxes.conf.cpu().numpy()
    coordinates = boxes.xyxy.cpu().numpy()
    
    object_indices = np.where(class_ids == object_class)[0]
    
    detections = []
    for idx in object_indices:
        detections.append({
            'box': coordinates[idx],  # [x1, y1, x2, y2]
            'confidence': float(confidences[idx]),
            'class_id': int(class_ids[idx]),
            'class_name': result.names[int(class_ids[idx])]
        })
    
    return detections


if __name__ == "__main__":
    # Example usage
    import cv2
    
    # Test with an image
    # image = cv2.imread('path/to/your/image.jpg')
    # boxes = detect_objects(image, 'book', confidence_threshold=0.3)
    # print(f"Detected {len(boxes)} books")
    # print(f"Bounding boxes:\n{boxes}")
    
    # Or with detailed info
    # detections = detect_objects_with_details(image, 'book')
    # for i, det in enumerate(detections):
    #     print(f"Book {i+1}: confidence={det['confidence']:.2f}, box={det['box']}")
    
    pass