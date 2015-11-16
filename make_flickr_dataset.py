import pandas as pd
import numpy as np
import os
import cPickle
from taeksoo.cnn_util import *
from sklearn.feature_extraction.text import CountVectorizer


vgg_model = '/home/taeksoo/Package/caffe/models/vgg/VGG_ILSVRC_19_layers.caffemodel'
vgg_deploy = '/home/taeksoo/Package/caffe/models/vgg/VGG_ILSVRC_19_layers_deploy.prototxt'

annotation_path = './data/results_20130124.token'
flickr_image_path = '../show_attend_and_tell/images/flickr30k/'
feat_path = './data/feats.npy'

cnn = CNN(model=vgg_model, deploy=vgg_deploy, width=224, height=224)

annotations = pd.read_table(annotation_path, sep='\t', header=None, names=['image', 'caption'])
annotations['image_num'] = annotations['image'].map(lambda x: x.split('#')[1])
annotations['image'] = annotations['image'].map(lambda x: os.path.join(flickr_image_path,x.split('#')[0]))

if not os.path.exists(feat_path):
    feats = cnn.get_features(annotations['image'].values)
    np.save(feat_path, feats)

captions = annotations['caption'].values

vectorizer = CountVectorizer(max_features=3000 - 3, token_pattern='\\b\\w+\\b').fit(captions)
dictionary = vectorizer.vocabulary_
dictionary = pd.Series(dictionary) + 3

dictionary['#END#'] = 0
dictionary['UNK'] = 1
dictionary['#START#'] = 2

with open('./data/dictionary.pkl', 'wb') as f:
    cPickle.dump(dictionary, f)
with open('./data/vectorizer.pkl', 'wb') as f:
    cPickle.dump(vectorizer, f)
