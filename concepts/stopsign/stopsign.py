
import numpy as np
import tensorflow as tf
from PIL import Image
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob

# From tensorflow models
from utils import label_map_util
from utils import visualization_utils as vis_util

# Constants
PATH_TO_CKPT = './frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
#IMAGE_PATH = './images/'
IMAGE_PATH = './video/'
NUM_CLASSES = 1
IMAGE_SIZE = (6,4)

# Helper functions
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# ----------------------------------------------------------------------------
# ---------- Initialization of the stop sign detection algorithm -------------
# ----------------------------------------------------------------------------

# Load the model
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Load the labels
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# ----------------------------------------------------------------------------
# ---------- Do the stop sign classification
# ----------------------------------------------------------------------------

# Initialize the image viewer
fig = plt.figure(figsize=IMAGE_SIZE)
plt.ion()
plt.show()

# Run the object detection
with detection_graph.as_default():
    # --- Input and output for the tensors
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Load the images
images_path = glob.glob(IMAGE_PATH + '*.jpg', recursive=False)
for image_path in images_path:
    image_path_one = image_path

def image_iterator():
    for image_path in images_path:
        before = datetime.datetime.now()
        image = Image.open(image_path)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        time_taken = datetime.datetime.now() - before
        print("Time taken to load image: " + str(time_taken))
        yield  image_np_expanded, image_np
    yield None, None

iter_ = image_iterator()

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # --- Run it on the image
        # Actual detection.

        while True:
            before = datetime.datetime.now()

            image_np_expanded, _image_np = iter_.__next__()
            if image_np_expanded is None:
                break
            image_np = _image_np
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            # Show the results
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            plt.imshow(image_np)
            plt.pause(0.0001)

            time_taken = datetime.datetime.now() - before
            print ("Time taken: " + str(time_taken))

input("Press Enter to continue...")