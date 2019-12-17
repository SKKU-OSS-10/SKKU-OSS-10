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
#import csv
import json
import io
#f=open('imageoutput.csv','a',encoding="utf-8",newline="")
#wr=csv.writer(f)

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

#imgurl = 'https://firebasestorage.googleapis.com/v0/b/perfectcody-d2e77.appspot.com/o/userPhoto%2FLc6VZDNYt2fjYcP5RY8Ez2IXOXo2%2Fmodel3.jpg?alt=media&token=9594ef3e-6805-4d1e-a98a-3fb349557f7'
#imgurl=sys.argv[1]
#urllib.request.urlretrieve(imgurl, 'image.jpg')
#img_name = 'test'+str(i)



path = '/home/bigdatalab/Downloads/SKKU-OSS-10/Dataset/Trainingset/MSS-2016'
img_list = os.listdir(path)
try:
    os.remove('./sample_images/json/MSS_2016.json')
except:
    pass
for i in range(192, len(img_list) + 1):#20191- 909 kill
    print(i);
    img_path = '/home/bigdatalab/Downloads/SKKU-OSS-10/Dataset/Trainingset/MSS-2016/'+str(i)+'.jpg'

    img_path = os.path.join(img_path)
    img = Image.open(img_path).convert("RGB")
    #back_removed_img = remove_background(img)

    #cropping = upper_lower_detection(back_removed_img)
    cropping=upper_lower_detection(img)
    trans = transforms.ToTensor()
    img = trans(img)
    img = img.mul(255).permute(1, 2, 0).byte().numpy()


    upper_categorise = [2,4]
    category_list = ['short_sleeve_top', 'long_sleeve_top','short_sleeve_outwear','long_sleeve_outwear','vest','sling','shorts','trousers','skirt','short_sleeve_dress','long_sleeve_dress','vest_dress','sling_dress' ]
    for idx in range(len(cropping)):
        cropped_img = cropping[idx]['cropping']
        color = get_color(cropped_img)
        cropped_img = Image.fromarray(cropped_img)
        boxes = cropping[idx]['boxes']
        labels = cropping[idx]['label']


        if cropping[idx]['label'] in upper_categorise:
            upper_pattern_pred = upper_pattern_detection(cropped_img)
            #print(upper_pattern_pred)
            cv2.putText(img, upper_pattern_pred, (boxes[0]+15, boxes[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

            upper_category_pred = upper_category_detection(cropped_img)
            #print(upper_category_pred)
            cv2.putText(img, upper_category_pred, (boxes[0] + 15, boxes[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (200, 200, 0), 2)
        else:
            upper_category_pred="."
            upper_pattern_pred="."

        img = cv2.rectangle(img, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (0, 255, 0), 2)

        name = category_list[labels-1]

        cv2.putText(img, name, (boxes[0], boxes[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)
        cv2.putText(img, str(color), (boxes[0], boxes[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

        #wr.writerow([img_name,boxes[0],boxes[1],boxes[2],boxes[3],name, labels-1,color[0],color[1],color[2],upper_category_pred,upper_pattern_pred])

    b, g, r = cv2.split(img)
    rimg = cv2.merge([r, g, b])

    #cv2.imwrite('sample_images/results/'+img_name+'.jpg', rimg)
    cv2.imwrite('/home/bigdatalab/Downloads/SKKU-OSS-10/Dataset/Trainingset/results/MSS-2016/' +  str(i) + '.jpg', rimg)
    try:
        info=dict()

        #print(boxes[0],boxes[1],boxes[2],boxes[3])
        info["input_Type"]=labels-1
        info["input_R"]=int(color[0])
        info["input_G"]=int(color[1])
        info["input_B"]=int(color[2])
        
        info["input_topType"]=upper_category_pred
        info["input_topPattern"]=upper_pattern_pred
        
        info["user_sex"]= 0
        info["user_style"]=0
        
        print(info)
        with io.open('./sample_images/json/MSS_2016.json','a',encoding='utf-8') as make_file:
            if i==1:
                make_file.write(unicode('[', 'utf-8'))
            make_file.write(str(json.dumps(info, indent=4, ensure_ascii=False)))
            if i!=len(img_list):
                make_file.write(unicode(',', 'utf-8'))
            else:
                make_file.write(unicode(']', 'utf-8'))
#            json.dump(info, make_file, indent='\t', ensure_ascii=False)
        
    except Exception:
        traceback.print_exc()
        print("not detect image")
    #cv2.imshow('img', rimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    '''img = cv2.rectangle(img, (boxes[0],boxes[1]),(boxes[2], boxes[3]), (0,255,0),2)

            cv2.putText(img, str(labels),(boxes[0],boxes[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)''' 