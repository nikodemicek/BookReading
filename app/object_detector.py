from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Create config
cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"

cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")

def detect_objects(image, object_class):
    """
    Detects objects in an image.

    Parameters
    ----------
    image : numpy.ndarray
        The image to process.

    Returns
    -------
    book_boxes : numpy.ndarray
        The bounding boxes of the detected objects.
    """
    # Make prediction
    predictor = DefaultPredictor(cfg)
    outputs = predictor(image)

    object_indices = [i for i, label in enumerate(outputs["instances"].pred_classes) if label == object_class]
    object_boxes = outputs["instances"].pred_boxes.tensor[object_indices]

    return object_boxes