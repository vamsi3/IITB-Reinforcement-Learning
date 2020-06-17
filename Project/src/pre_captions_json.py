# encoding: UTF-8

import os
import json
import numpy as np
import cPickle as pickle
from tqdm import tqdm

captions_path = './data/videodatainfo_2017.json'
save_train_captions_path = './data/train_captions.pkl'
save_val_captions_path = './data/val_captions.pkl'
save_test_captions_path = './data/test_captions.pkl'

captions_json = json.load(open(captions_path))


train_captions = {}
val_captions = {}
test_captions = {}

for i in range(10000):
    if i<6513:
        train_captions['video'+str(i)] = []
    elif i<7010 and i>=6513:
        val_captions['video'+str(i)] = []
    elif i>=7010:
        test_captions['video'+str(i)] = []

all_captions = captions_json['sentences']
#print(test_captions['video7010'])
#exit()
for meta_caption in tqdm(all_captions):
    cap = meta_caption['caption']
    cap = cap.lower()
    cap = cap.replace('.', '')
    cap = cap.replace(',', ' ,')
    cap = cap.replace('?', ' ?')
    vid_id = meta_caption['video_id']
    vid = int(vid_id[5:])
    if vid<6513:
        train_captions[vid_id].append(cap)
    elif vid<7010 and vid>=6513:
        val_captions[vid_id].append(cap)
    elif vid>=7010:
        test_captions[vid_id].append(cap)


with open(save_train_captions_path, 'w') as fw:
    pickle.dump(train_captions, fw)

with open(save_val_captions_path, 'w') as fw:
    pickle.dump(val_captions, fw)

with open(save_test_captions_path, 'w') as fw:
    pickle.dump(test_captions, fw)

"""
image_ids = []
for annotation in train_captions['annotations']:
    image_ids.append(annotation['image_id'])

# [[filename1, id1], [filename2, id2], ... ]
images_captions = {}
for ii, image in enumerate(train_captions['images']):
    start_time = time.time()

    image_file_name = image['file_name']
    image_id = image['id']
    indices = [i for i, x in enumerate(image_ids) if x == image_id]

    caption = []
    for idx in indices:
        each_cap = train_captions['annotations'][idx]['caption']
        each_cap = each_cap.lower()
        each_cap = each_cap.replace('.', '')
        each_cap = each_cap.replace(',', ' ,')
        each_cap = each_cap.replace('?', ' ?')
        caption.append(each_cap)
    images_captions[image_file_name] = caption
    print "{}  {}  Each image cost: {}".format(ii, image_file_name, time.time()-start_time)
"""
