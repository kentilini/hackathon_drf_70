#!/usr/bin/env python2

import time
import argparse
import cv2
import itertools
import os
import numpy as np
import openface

np.set_printoptions(precision=2)

align = openface.AlignDlib("shape_predictor_68_face_landmarks.dat")
net = openface.TorchNeuralNet("nn4.small2.v1.t7", 96)


def get_rep(img_path):
    bgr_img = cv2.imread(img_path)
    if bgr_img is None:
        raise Exception("Unable to load image: {}".format(img_path))
    rgb_mg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    bb = align.getLargestFaceBoundingBox(rgb_mg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(img_path))
    aligned_face = align.align(96, rgb_mg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if aligned_face is None:
        raise Exception("Unable to align image: {}".format(img_path))
    rep = net.forward(aligned_face)

    print("Representation:")
    print(rep)
    print("-----\n")
    return rep
