# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 03:16:09 2019

@author: Hyunseung
"""

from sklearn import preprocessing
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import json

data = np.genfromtxt("output_modify.csv", delimiter=',', dtype=int)
data_str = np.genfromtxt("output_modify.csv", delimiter=',', dtype=str)

data1 = data[:,:5]
data2 = data[:,6:10]
le = preprocessing.LabelEncoder()
le.fit(data_str[:,10])
data3=np.array(le.transform(data_str[:,10]))

le2 = preprocessing.LabelEncoder()
le2.fit(data_str[:,11])
data4=np.array(le2.transform(data_str[:,11]))
data5= np.column_stack((data3,data4))

preProcessingData = np.concatenate((data1,data2,data5),axis=1)


input_data = open("input.json").read()
input_data = json.loads(input_data)


####input labels####


input_Type=int(input_data["input_Type"])
input_R=int(input_data["input_R"])
input_G=int(input_data["input_G"])
input_B=int(input_data["input_B"])
input_topType=int(input_data["input_topType"])
#hoodie:1, shirt:2 sweater:3 sweatshirt:4
input_topPattern=int(input_data["input_topPattern"])
#check:1 dot:2 printed:3 simple:4 stripe:5

user_sex=int(input_data["user_sex"])
#man=0, woman=1
user_style=int(input_data["user_style"])
#casual:0, dandy:1, street:2






'''
style_info = dict()
style_info["input_Type"]=input_Type
style_info["input_R"]=input_R
style_info["input_G"]=input_G
style_info["input_B"]=input_B
style_info["input_topType"]=input_topType
style_info["input_topPattern"]=input_topPattern
style_info["user_sex"]=user_sex
style_info["user_style"]=user_style
###################
with open('input.json','w',encoding='utf-8') as make_file:
    json.dump(style_info,make_file,indent='\t')
'''


style_list = np.genfromtxt('filelist.csv', delimiter=',',dtype=int)
style_list_for_user = style_list[style_list[:,1]==user_sex,:]
style_list_for_user = style_list_for_user[style_list_for_user[:,2]==user_style,:]
style_list_number=[]
for number in style_list_for_user:
    style_list_number.append(number[0])

selectedData = preProcessingData[preProcessingData[:,5]==input_Type,:]
selectedData = selectedData[selectedData[:,9]==input_topType,:]
selectedData = selectedData[selectedData[:,10]==input_topPattern,:]

rgb_difference = np.array([]).reshape(-1,2)
for i in range(len(selectedData)):
    temp= np.array([selectedData[i][0],((input_R-selectedData[i][6])**2+(input_G-selectedData[i][7])**2+(input_B-selectedData[i][8])**2)**0.5]).reshape(-1,2)
    rgb_difference= np.concatenate((rgb_difference,temp),axis=0)
    
rgb_difference = sorted(rgb_difference,key=lambda x:x[1])

bestlist=[]
for i in range(20):
    if rgb_difference[i][1]<20:
        if rgb_difference[i][0] in style_list_number:
            bestlist.append(int(rgb_difference[i][0]))


for i in bestlist:
    print(i,end=" ")
    #datapath="./sample_images/image/"+str(i)+".jpg"
    #img = mpimg.imread(datapath)
    #plt.imshow(img)
    #plt.show()
    
if len(bestlist)==0:
    print("No Cody in List")