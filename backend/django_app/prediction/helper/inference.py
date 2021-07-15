from tensorflow import keras
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd
import os
from typing import Union, Callable

os.environ["CUDA_VISIBLE_DEVICES"]="-1"

from io import BytesIO
import urllib

# Access temporary files
import tempfile

# Kmeans Color Palette
import faiss
from skimage import color


# fake visitor to overcome denied request
# Adding information about user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# img loader
def load_image(img_path, filename="temp.jpg"):
    TEMPDIR = tempfile.gettempdir()
    # Ensure that the file is saved to temp
    filename = TEMPDIR + '/' + filename

    try:
        urllib.request.urlretrieve(img_path, filename)

    except OSError:
        urllib.request.urlretrieve(TEMPDIR + '/' + img_path, filename)

    image_PIL = tf.keras.preprocessing.image.load_img(filename,
                                                grayscale=False, color_mode='rgb', target_size=(224,224),
                                                interpolation='nearest')

    image = tf.keras.preprocessing.image.img_to_array(image_PIL,
                                           data_format=None,
                                           dtype=None)

    image = tf.expand_dims(image, axis=0, name=None)

    os.remove(filename)
    return image

def stack_img(img_list):
    '''
    img_list = list of paths to imgs
    '''
    stacked = []

    # Init data for Kmeans
    rgb_list, hex_list = [], []
    # Define a function for the mapping in Kmeans
    rgb2hex = lambda r, g, b: '#%02x%02x%02x' % (r, g, b)

    for i in img_list:
        # Process Kmeans for each Image
        temp_color = faiss_kmeans(i)
        B = (temp_color*255).astype(int)  # convert to int
        rgb_list.append(B)
        hex_list.append(
            [rgb2hex(*B[i, :]) for i in range(B.shape[0])]
        )

        # Stack for each image
        stacked.append(load_image(i))

    input_y = np.vstack(stacked)

    return input_y, rgb_list, hex_list

def faiss_kmeans(img_path, filename="temp.jpg"):
    TEMPDIR = tempfile.gettempdir()
    # Ensure that the file is saved to temp
    filename = TEMPDIR + '/' + filename

    try:
        urllib.request.urlretrieve(img_path, filename)
    except OSError:
        urllib.request.urlretrieve(TEMPDIR + '/' + img_path, filename)

    with open(filename,"rb") as f:
        img = np.array(Image.open(f))

    rgb_pixels = img.reshape((-1, 3)).astype("float32") / 255

    # Convert RGB to HSV
    hsv_pixels = color.rgb2hsv(rgb_pixels)

    kmeans = faiss.Kmeans(d=hsv_pixels.shape[1],
                                       k=5)
    kmeans.train(hsv_pixels.astype(np.float32))
    cluster_centers_ = kmeans.centroids

    # Sort
    faiss_hsv_centers = np.sort(cluster_centers_, axis=0)

    faiss_rgb_centers = color.hsv2rgb(faiss_hsv_centers)

    return faiss_rgb_centers

if __name__ == "__main__":

    # predefine class names
    class_names = ['Contemporary',
    'Eclectic',
    'Industrial',
    'Kitchen',
    'Minimalistic',
    'Modern',
    'Retro',
    'Scandinavian',
    'Traditional',
    'Transitional',
    'Vintage']
    #find stacked vector from multiple images
    input_y = stack_img(img_list)

    #prediction
    prediction = predict_image(input_y, '../../../../../Users/antho/Desktop/linear_back/app/backend/django_app/prediction/mlmodel/models/styleclassifier.h5')
    predictions = pd.DataFrame(prediction, columns=class_names)
    sorted_cats = predictions.sum().sort_values(ascending=False).index
    print('Your prefered style is ' + sorted_cats[0:3][0] + ' with a mix of ' + sorted_cats[0:3][1] + ' and ' + sorted_cats[0:3][2])