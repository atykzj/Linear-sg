import os
import numpy as np
import pandas as pd
from PIL import Image
from glob import glob
import json
from tqdm import tqdm
from urllib.request import urlopen

os.environ["CUDA_VISIBLE_DEVICES"]="-1"   
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.applications.imagenet_utils import preprocess_input


class ImageRecommender : 
    
    def __init__(self, model, db_root): 
        #init model
        self.model = model
        #since ouput.shape return object dimension just eval it to get integer ...
        self.image_width = eval(str(self.model.layers[0].output.shape[1]))
        self.image_height = eval(str(self.model.layers[0].output.shape[2]))
        # remove the last layers in order to get features instead of predictions
        self.image_features_extractor = Model(inputs=self.model.input, outputs=self.model.layers[-2].output)
        self.db_root = db_root
        self.file_list = glob(self.db_root + '*.jpg')

    def load_db_dict(self):

        BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        js_root = os.path.join(BASE, 'models/')

        if 'https' in js_root:
            print('loading dict from url')
            response = urlopen(js_root + 'dict.json')
            data = json.loads(response.read())

        else:
            print('loading dict locally')
            with open(js_root + 'dict.json', 'r') as fp:
                data = json.load(fp)

        keys = list(data.keys())
        self.db_subset = [js_root + i for i in keys]
        self.db_features = list(data.values())

    def extract_db(self):
        """get all jpgs in pic db and returns a dictionary of img name and extracted features
        """
        print('converting to tensor')
        db_pics = self.PicstoTensor(self.file_list)
        print('extracting deature from ' + str(len(self.file_list) + 'files'))
        db_features = self.extract_features(db_pics)
        
        # create dictionary of filename:features
        print('creating dictionary')
        keys_list = [os.path.basename(f) for f in file_list]
        values_list = db_features.tolist()
        zip_iterator = zip(keys_list, values_list)
        dictionary = dict(zip_iterator)

        # save dict.json
        with open(self.db_root + 'dict.json', 'w') as fp:
            json.dump(dictionary, fp)
        print('dict.json saved at ' + self.db_root)

    def load_image(self, image_path):
        image_PIL = tf.keras.preprocessing.image.load_img(image_path, 
                                                        grayscale=False, color_mode='rgb', target_size=(self.image_height,self.image_width),
                                                        interpolation='nearest')
        image = tf.keras.preprocessing.image.img_to_array(image_PIL, 
                                                        data_format=None, dtype=None)
        image = tf.expand_dims(image, axis=0, name=None)
        return image

    def PicstoTensor(self, list_of_image):
        """stack pics to batch
        """
        img_list =[]
        for i in tqdm(list_of_image):
            img_list.append(self.load_image(i))
            self.stacked_input = np.vstack(img_list)
        return self.stacked_input
    
    def extract_features(self, stacked_imgs):
        stacked_imgs = preprocess_input(stacked_imgs)
        self.imgs_features = self.image_features_extractor.predict(stacked_imgs)
        return self.imgs_features
        
    def GetSimilarity(self, imgs_features, list_of_image):
        cosSimilarities = cosine_similarity(imgs_features)
        cos_similarities_df = pd.DataFrame(cosSimilarities, 
                                           columns=list_of_image[:len(list_of_image)],
                                           index=list_of_image[:len(list_of_image)])
        return cos_similarities_df
    
    def find_similar(self, stacked_imgs, nb_closest_images=8):
        """extract features from a batch of img and returns paths to similar imgs
        
        Parameters:
        stacked_imgs (tensor): batch of imgs
        nb_closest_images (int): top k imgs to return
        
        Returns:
        closest_imgs (list): path to imgs
        """
        imgs_features = self.extract_features(stacked_imgs)
        imgs_features = np.mean(imgs_features, axis=0)
        imgs_features = tf.expand_dims(imgs_features, axis=0)
        
        final_features = np.append(self.db_features, imgs_features, axis=0)
        final_list = self.db_subset + ['input']

        sim_table = self.GetSimilarity(final_features, final_list)
        closest_imgs = sim_table['input'].sort_values(ascending=False)[1:nb_closest_images+1].index
        return closest_imgs