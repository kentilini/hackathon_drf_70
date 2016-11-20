#!/usr/bin/env python2

import time
import argparse
import cv2
import itertools
import os
import numpy as np
import openface
import sys
import getopt
import json
import math

np.set_printoptions(precision=2)

align = openface.AlignDlib("shape_predictor_68_face_landmarks.dat")
net = openface.TorchNeuralNet("nn4.small2.v1.t7", 96)
images_dir = './images/preps/'
json_path_pattern = './images/preps/{}/data.json'

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

    return rep


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        sys.exit(2)
    #data = read_data_from_file(args[0])

    get_best_match(args[0])

#    print_images_data(images_dir)

def read_data_from_file(aFile):
    if not os.path.isfile(aFile):
        print_images_data(images_dir, aFile)
    with open(aFile) as file:
        data = [split([float(digit) for digit in line.split()],128) for line in file]
    return data

def get_best_match(img_path):
    results = np.array(compare_image_with_data(img_path))
    print results    
    ind = np.argpartition(results, 9)[:10]
    ind = ind[np.argsort(results[ind])]
    print ind

    if results[ind[0]] > 0.3:
        return None

    data = []
 
    for i in ind:
        fPath = json_path_pattern.format(i)
        with open(fPath) as data_file:
            data.append(json.load(data_file))
    return data[0]

def compare_image_with_data(img_path):
    image_rep = get_rep(img_path)

#    print 'image distance ', 
#    print image_rep

    result = []
    for vect in data:
        sum = 0
        for el in vect[1:]:
            sum += math.sqrt(np.dot(image_rep - el, image_rep - el))
        result.append(sum/(len(vect)-1))

   # return [np.dot(el[0] - image_rep, el[0] - image_rep) for el in data] 
    return result

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs    

def print_images_data(dir_path, output):
    out_f = open(output, 'w')

    only_dirs = [ f for f in os.listdir(dir_path) if not os.path.isfile(str.join(dir_path, f))]
    only_dirs.sort(key=float)

    print only_dirs
    for dir in only_dirs:
        print dir
        everage, aList = get_folder_everage(os.path.join(dir_path,dir))
        for el in everage:
            out_f.write(str(el))
            out_f.write(' ')
        for arr in aList:
            for el in arr: 
                out_f.write(str(el))
                out_f.write(' ')
        out_f.write('\r\n')
    out_f.close()        

def get_folder_everage(dir_path):
#    print dir_path
    total = 0;
    count = 0;
    aList = [];
    for dirpath,_,files in os.walk(dir_path):
        filenames = [ file for file in files if not os.path.join(dirpath, file).endswith( ('.json') ) ] 
        
 #       print files
 #       print filenames
        for f in filenames:
             distance = get_rep( os.path.abspath(os.path.join(dirpath, f)))
             aList.append(distance)
             total += distance 
             count += 1
    return np.asarray(total/count), aList


data = read_data_from_file('./data.txt')
if __name__ == "__main__":
    main()
