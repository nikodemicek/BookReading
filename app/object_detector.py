from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Create config
cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"

cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")

def detect_books(image):
    """
    Detects books in an image.

    Parameters
    ----------
    image : numpy.ndarray
        The image to process.

    Returns
    -------
    book_boxes : numpy.ndarray
        The bounding boxes of the detected books.
    """
    # Make prediction
    predictor = DefaultPredictor(cfg)
    outputs = predictor(image)

    # Filter predictions for books (book class in COCO dataset is 73)
    book_indices = [i for i, label in enumerate(outputs["instances"].pred_classes) if label == 73]
    book_boxes = outputs["instances"].pred_boxes.tensor[book_indices]

    return book_boxes
