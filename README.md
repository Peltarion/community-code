# tagger-tutorial
This is a repo with accompanying code for the tutorial "Predicting mood from raw audio data" https://peltarion.com/knowledge-center/tutorials/predicting-mood-from-raw-audio-data

The notebook "tagger-tutorial-all-code.ipynb" takes you through all the transforms needed to turn .mp3 files into a .png file (a STFT mel spectrogram) ready for a convolutional neural network to tag it with corresponding moods from the training set. It is a multiclass classification and you call the resulting model via a rest endpoint. We use a JSON method via requests, ready to batch up multiple requests as one call. 

You can create your own classifier *on your own data* and create something awesome in very little time. Have a look at our trial at https://peltarion.com/