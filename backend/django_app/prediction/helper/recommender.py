import numpy as np
import pandas as pd
from glob import glob
import json
from urllib.request import urlopen

import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"   

class ImageRecommender : 
    """An Image Recommender class that extracts the feature vectors from
    a list of images and compare the cosine similarity with features in the pre-extracted database. 

    Returns: URLS to recommended images hosted on GCP
    """
    def __init__(self, model, db_root, cloud_dir): 
        """Constructs all neccessary attributes required by the extractor

        Args:
            input (list): list of URLs of images
            model (TF.Model): TF model with GlobalAveragePooling Layer as the Top Layer
            db_root (str): Path to image root folder
            cloud_dir ([type]): root URL to the cloud bucket
        """
        self.db_root = db_root
        self.cloud_dir = cloud_dir
        self.file_list = glob(self.db_root + '*.jpg')
        self.image_size = (224,224)
        self.extractor_model = model
        
    def load_db_dict(self, db_name='dict.json'):
        """loads a dictionary of extracted image features from a json file

        Args:
            db_name (str, optional): path to dictionary.json. Defaults to 'dict.json'.
        """
        if 'https' in self.db_root:
            print('loading dict from url')
            response = urlopen(self.db_root + db_name)
            data = json.loads(response.read())

        else:
            print('loading dict locally')
            with open(self.db_root + db_name, 'r') as fp:
                data = json.load(fp)

        keys = list(data.keys())
        self.db_subset = [self.cloud_dir + i for i in keys]
        self.db_features = list(data.values())
        print(str(len(self.db_features)) + ' features loaded')

    def get_similarity_table(self, imgs_features, list_of_image):
        """computes cosine similarity of extracted features with the loaded features in database"""
        cosSimilarities = cosine_similarity(imgs_features)
        cos_similarities_df = pd.DataFrame(cosSimilarities, 
                                           columns=list_of_image[:len(list_of_image)],
                                           index=list_of_image[:len(list_of_image)])
        return cos_similarities_df
    
    def find_similar(self, stacked_imgs, nb_closest_images=6):
        """extract features from a batch of img and returns paths to similar imgs
        
        Parameters:
        nb_closest_images (int): top n imgs to return
        
        Returns:
        closest_imgs (list): path to imgs on cloud bucket
        """

        imgs_features = self.extractor_model.predict(stacked_imgs)
        imgs_features = np.mean(imgs_features, axis=0)
        imgs_features = tf.expand_dims(imgs_features, axis=0)
        
        final_features = np.append(self.db_features, imgs_features, axis=0)
        final_list = self.db_subset + ['input']

        sim_table = self.get_similarity_table(final_features, final_list)
        closest_imgs = sim_table['input'].sort_values(ascending=False)[1:nb_closest_images+1].index
        return closest_imgs