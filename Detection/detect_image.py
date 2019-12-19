#-*- coding: utf-8 -*-
from upper_lower_detection import *
from upper_pattern_classification import *
from upper_category_detection import *
from remove_background import *
from PIL import Image
import os, cv2
from torchvision import transforms
import numpy as np
import sys
import traceback
import csv
import json
import io

#RGB
def get_color(img):
    idx = []
    data = np.reshape(img, (-1,3))
    for i in range(data.shape[0]):
        if np.all(data[i] == [0,0,0]):
            idx.append(i)
    idx.reverse()
    data = data.tolist()
    for i in idx:
        data.pop(i)

    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)
    return centers[0].astype(np.int32)[::-1]


def detect_image(path):

    f=open('imageoutput.csv','w')
    wr=csv.writer(f)
    img = Image.open(path).convert("RGB")
    cropping=upper_lower_detection(img)
    trans = transforms.ToTensor()
    img = trans(img)
    img = img.mul(255).permute(1, 2, 0).byte().numpy()


    upper_categorise = [0, 1, 2, 3, 4]
    category_list = ['short_sleeve_top', 'long_sleeve_top','short_sleeve_outwear','long_sleeve_outwear','vest','sling','shorts','trousers','skirt','short_sleeve_dress','long_sleeve_dress','vest_dress','sling_dress' ]


    for idx in range(len(cropping)):
        cropped_img = cropping[idx]['cropping']
        color = get_color(cropped_img)
        cropped_img = Image.fromarray(cropped_img)
        boxes = cropping[idx]['boxes']
        labels = cropping[idx]['label']


        if cropping[idx]['label'] in upper_categorise:
            pattern_pred = upper_pattern_detection(cropped_img)
            #print(upper_pattern_pred)
#            cv2.putText(img, pattern_pred[idx], (boxes[0]+15, boxes[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

            category_pred = upper_category_detection(cropped_img)
            #print(upper_category_pred)
#            cv2.putText(img, category_pred[idx], (boxes[0] + 15, boxes[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
#                        (200, 200, 0), 2)
        else:
            category_pred = "."
            pattern_pred = "."

#        img = cv2.rectangle(img, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (0, 255, 0), 2)

        name = category_list[labels-1]

#        cv2.putText(img, name, (boxes[0], boxes[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)
#        cv2.putText(img, str(color), (boxes[0], boxes[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

        wr.writerow([1, boxes[0], boxes[1], boxes[2], boxes[3], name, labels-1,
                     color[0], color[1], color[2], category_pred, pattern_pred])
    
    return

if __name__ == "__main__":
    detect_image(sys.argv[1])
