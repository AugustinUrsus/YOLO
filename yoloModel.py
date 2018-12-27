import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import scipy.io
import scipy.misc
import numpy as np
import pandas as pd
import PIL
import tensorflow as tf
from keras import backend as K
from keras.layers import Input, Lambda, Conv2D
from keras.models import load_model, Model
from yolo_utils import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes, scale_boxes
from yad2k.models.keras_yolo import yolo_head, yolo_boxes_to_corners, preprocess_true_boxes, yolo_loss, yolo_body

def yolo_filter_boxes(box_confidence, boxes, box_class_probs, threshold = .6):

    box_scores = box_confidence * box_class_probs

    box_classes = K.argmax(box_scores, axis = -1)
    box_class_scores = K.max(box_scores, axis = -1)


    filtering_mask = box_class_scores >= threshold

    scores = tf.boolean_mask(tensor = box_class_scores, mask = filtering_mask)
    boxes = tf.boolean_mask(tensor = boxes, mask = filtering_mask)
    classes = tf.boolean_mask(tensor = box_classes, mask = filtering_mask)

    return scores, boxes, classes

with tf.Session() as test_a:

    box_confidence = tf.random_normal([19, 19, 5, 1], mean = 1, stddev = 4, seed = 1)
    boxes = tf.random_normal([19, 19, 5, 4], mean = 1, stddev = 4, seed = 1)
    box_class_probs = tf.random_normal([19, 19, 5, 80], mean = 1, stddev = 4, seed = 1)
    scores, boxes, classes = yolo_filter_boxes(box_confidence, boxes, box_class_probs, threshold = 0.5)
    print('scores[2] = ' + str(scores[2].eval()))
    print('boxes[2] = ' + str(boxes[2].eval()))
    print('classes[2] = ' + str(classes[2].eval()))
    print('scores.shape = ' + str(boxes.shape))
    print('boxes.shape = ' + str(boxes.shape))
    print('classes.shape = ' + str(classes.shape))


