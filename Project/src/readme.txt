Requirements to run experiments:
tensorflow 1.14
cPickle

Extract frames from the videos and then extract features from them by using resnet-152 pretrained on ImageNet dataset.

run pre_captions_json.py to extract captions from the json file and store them in a pickle file
run build_vocab.py to form idx_to_word.npy and word_to_idx.npy files
run create_train_val_all_reference.py to create a json file that contains the GT captions as required by the coco evaluation scripts
run create_train_val_each_reference.py to create json files separately for every video that contains the GT captions as required by the coco evaluation scripts while using Train_Bphi_Model from video_captioning.py

------------Training-------------
run Train_with_MLE from video_captioning.py to train the model using only cross_entropy loss (This step is required fro good initialization)

run Sample_Q_with_MC from video_captioning.py which simulate Monte Carlo rollouts to estimate Q function
run Train_Bphi_Model from video_captioning.py to train the baseline model
run Train_SGD_update from video_captioning.py to run the main training loop as mentioned in the report

------------Testing---------------
you can evaluate any model just by changing the checkpoint file in Test_with_MLE from video_captioning.py 
predicted sentences for the MLE model are in test_results_MLE.txt
predicted sentences for the RL model are in test_results_rl.txt

To get the scores run eval_model.py by making appropriate changes in the file
