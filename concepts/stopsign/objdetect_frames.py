
import tensorflow as tf
import numpy as np
import datetime
import cv2

# From tensorflow models
from utils import label_map_util
from utils import visualization_utils as vis_util

PATH_TO_CKPT = './frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
VIDEO_PATH = './video/stopsigns.mp4'
NUM_CLASSES = 1
IMAGE_SIZE = (6,4)

# Helper functions
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def generate_frames(a,v, done_decoding):
    # Load the video
    vid = cv2.VideoCapture(VIDEO_PATH)

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
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

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

        with tf.Session(graph=detection_graph) as sess:
            # --- Run it on the image
            # Actual detection.

            while True:
                before = datetime.datetime.now()

                ret, image = vid.read()
                if (ret == False):
                    break

                image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)

                if image_np_expanded is None:
                    break

                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # This is the time taken to run the detection
                time_taken = datetime.datetime.now() - before
                print("Time taken to run detection: " + str(time_taken))

                # Show the results
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                #image_np = cv2.resize(image_np, (infoObject.current_w, infoObject.current_h))

                memoryview(a).cast('B')[:] = image_np.flatten()

                # Increment a frame number
                v.value = v.value + 1

                time_taken = datetime.datetime.now() - before
                print ("Time taken: " + str(time_taken))