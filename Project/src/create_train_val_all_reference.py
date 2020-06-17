# encoding: UTF-8

import os
import glob
import json
import cPickle as pickle


train_val_imageNames_to_imageIDs = {}
train_val_Names_Captions = []
#train_imageNames_to_imageIDs = {}
#val_imageNames_to_imageIDs = {}
given_list = pickle.load(open('./data/video_list.pkl'))

################################################################
save_train_captions_path = './data/train_captions.pkl'
save_val_captions_path = './data/val_captions.pkl'
save_test_captions_path = './data/test_captions.pkl'
train_captions = pickle.load(open(save_train_captions_path,'rb'))
val_captions = pickle.load(open(save_val_captions_path,'rb'))
test_captions = pickle.load(open(save_test_captions_path,'rb'))

for i in given_list:
	idx = 'video'+str(i)
	train_val_imageNames_to_imageIDs[idx] = idx
	if i<6513:
		cap_list = train_captions[idx]
		for sent in cap_list:
			train_val_Names_Captions.append([idx, sent])
	if i>=6513 and i<7010:
		cap_list = val_captions[idx]
		for sent in cap_list:
			train_val_Names_Captions.append([idx, sent])
	if i>=7010:
		cap_list = test_captions[idx]
		for sent in cap_list:
			train_val_Names_Captions.append([idx, sent])
    

#################################################################

json_fw = open('./data/temp_reference.json', 'w')
json_dict = {}
json_dict["info"] = dict({"description": "Test", "url": "", "version": "1.0", "year": 2019, "contributor": "", "date_created": "2019"})
json_dict["images"] = []
count = 0
for imageName, imageID in train_val_imageNames_to_imageIDs.iteritems():
	int_dict = {}
	int_dict["license"] = 1
	int_dict["file_name"] = str(imageName)
	int_dict["id"] = str(imageID)
	json_dict["images"].append(int_dict)
	count += 1

#json_fw.write(', "licenses": [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/", "id": 1, "name": "Test"}], ')
json_dict["licenses"] = [dict({"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/", "id": 1, "name": "Test"})]
json_dict["type"] = "captions"
#json_fw.write('"type": "captions", "annotations": [')
json_dict["annotations"] = []
flag_count = 0
id_count = 0
for imageName, imageID in train_val_imageNames_to_imageIDs.iteritems():
	#print "{},  {},  {}".format(flag_count, imageName, imageID)

	captions = []
	for item in train_val_Names_Captions:
		if item[0] == imageID:
			captions.append(item[1])


	for idx, each_sent in enumerate(captions):
		int_dict = {}
		if '\n' in each_sent:
			each_sent = each_sent.replace('\n', '')
		if '\\' in each_sent:
			each_sent = each_sent.replace('\\', '')
		if '"' in each_sent:
			each_sent = each_sent.replace('"', '')
		#if flag_count==1997:
		#	print(each_sent)
		int_dict["image_id"]=str(imageID)
		int_dict["id"]=str(id_count)
		id_count += 1
		int_dict["caption"] = each_sent.encode("ascii","ignore")
		json_dict["annotations"].append(int_dict)

json.dump(json_dict,json_fw)	
json_fw.close()
