#!/usr/bin/env python
# coding=utf-8
import os
import json
import cPickle as pickle
import io
test_results_save_path = 'test2014_results_model-486.txt'
test_results = open(test_results_save_path).read().splitlines()

images_captions = {}
captions = []
names = []
for idx, item in enumerate(test_results):
    if idx % 2 == 0:
        names.append(item)
    if idx % 2 == 1:
        captions.append(item)

for idx, name in enumerate(names):
    print idx, ' ', name
    images_captions[name] = captions[idx]

val2014_images_ids_to_names = {}
for i in range(7010,10000):
    val2014_images_ids_to_names['video'+str(i)] = 'video'+str(i)

names_to_ids = {}
for key, item in val2014_images_ids_to_names.iteritems():
    names_to_ids[item] = key

fw_1 = open('coco-caption/captions_val2014_results.json', 'w')
#fw_1.write('[')
json_dict = []
for idx, name in enumerate(names):
    print idx, ' ', name
    tmp_idx = names.index(name)
    caption = captions[tmp_idx]
    caption = caption.replace(' ,', ',')
    caption = caption.replace('"', '')
    caption = caption.replace('\n', '')
    int_dict = {}
    int_dict["image_id"] = str(names_to_ids[name])
    int_dict["caption"] = str(caption)
    json_dict.append(int_dict)
        
json.dump(json_dict,fw_1)