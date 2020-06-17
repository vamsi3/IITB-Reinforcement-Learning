# encoding: UTF-8

###############################################################
#
# generate images captions into every json file one by one,
# and get the dict that map the image IDs to image Names
#
###############################################################

import os
import sys
import json
import cPickle as pickle

train_val_imageNames_to_imageIDs = {}
train_imageNames_to_imageIDs = {}
val_imageNames_to_imageIDs = {}
train_Names_Captions = []
save_train_captions_path = './data/train_captions.pkl'
train_captions = pickle.load(open(save_train_captions_path))
for i in range(6513):
	idx = 'video'+str(i)
	train_imageNames_to_imageIDs[idx] = idx
	cap_list = train_captions[idx]
	for sent in cap_list:
		train_Names_Captions.append([idx, sent])

train_count = 0
for imageName, imageID in train_imageNames_to_imageIDs.iteritems():
	print "{},  {},  {}".format(train_count, imageName, imageID)
	train_count += 1

	captions = []
	for item in train_Names_Captions:
		if item[0] == imageID:
			captions.append(item[1])

	json_fw = open('./train_val_reference_json/'+imageName+'.json', 'w')
	json_dict = {}
	json_dict["info"] = {"description": "CaptionEval", "url": "", "version": "1.0", "year": 2019, "contributor": "", "date_created": "2019"}
	json_dict["images"] = [{"license": 1, "file_name": imageName , "id": str(imageID)}]
	json_dict["licenses"] = [{"url": "test", "id": 1, "name": "test"}]
	json_dict["type"] = "captions"
	json_dict["annotations"] = []

	id_count = 0
	for idx, each_sent in enumerate(captions):
		int_dict = {}
		
		if '\n' in each_sent:
			each_sent = each_sent.replace('\n', '')
		if '\\' in each_sent:
			each_sent = each_sent.replace('\\', '')
		if '"' in each_sent:
			each_sent = each_sent.replace('"', '')
		int_dict["image_id"]=str(imageID)
		int_dict["id"]=str(id_count)
		int_dict["caption"] = each_sent.encode("ascii","ignore")
		json_dict["annotations"].append(int_dict)
	json.dump(json_dict,json_fw)
	

# Validation json file
save_val_captions_path = './data/val_captions.pkl'
val_Names_Captions = []
val_captions = pickle.load(open(save_val_captions_path))
for i in range(6513,7010):
	idx = 'video'+str(i)
	val_imageNames_to_imageIDs[idx] = idx
	cap_list = val_captions[idx]
	for sent in cap_list:
		val_Names_Captions.append([idx, sent])

val_count = 0
for imageName, imageID in val_imageNames_to_imageIDs.iteritems():
	print "{},  {},  {}".format(val_count, imageName, imageID)

	captions = []
	for item in val_Names_Captions:
		if item[0] == imageID:
			captions.append(item[1])

	json_fw = open('./train_val_reference_json/'+imageName+'.json', 'w')
	json_dict = {}
	json_dict["info"] = {"description": "CaptionEval", "url": "", "version": "1.0", "year": 2019, "contributor": "", "date_created": "2019"}
	json_dict["images"] = [{"license": 1, "file_name": imageName , "id": str(imageID)}]
	json_dict["licenses"] = [{"url": "test", "id": 1, "name": "test"}]
	json_dict["type"] = "captions"
	json_dict["annotations"] = []

	id_count = 0
	for idx, each_sent in enumerate(captions):
		int_dict = {}
				
		if '\n' in each_sent:
			each_sent = each_sent.replace('\n', '')
		if '\\' in each_sent:
			each_sent = each_sent.replace('\\', '')
		if '"' in each_sent:
			each_sent = each_sent.replace('"', '')
		int_dict["image_id"]=str(imageID)
		int_dict["id"]=str(id_count)
		int_dict["caption"] = each_sent.encode("ascii","ignore")
		json_dict["annotations"].append(int_dict)
	json.dump(json_dict,json_fw)
	json_fw.close()

for k, item in train_imageNames_to_imageIDs.iteritems():
	train_val_imageNames_to_imageIDs[k] = item
for k, item in val_imageNames_to_imageIDs.iteritems():
	train_val_imageNames_to_imageIDs[k] = item

with open('./data/train_val_imageNames_to_imageIDs.pkl', 'w') as fw_2:
	pickle.dump(train_val_imageNames_to_imageIDs, fw_2)


