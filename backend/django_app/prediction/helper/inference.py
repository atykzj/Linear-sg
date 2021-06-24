from tensorflow import keras
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd
import os 
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

from io import BytesIO
import urllib

# Access temporary files
import tempfile


# fake visitor to overcome denied request
# Adding information about user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# img loader
def load_image(img_path, model_type, filename="temp.jpg"):
    TEMPDIR = tempfile.gettempdir()
    # Ensure that the file is saved to temp
    filename = TEMPDIR + '/' +filename

    # try:
    #     # normal retrieval
    #     image_raw = urllib.request.urlopen(img_path).read()
    # except:
    # fake visitor to overcome denied request
    # Adding information about user agent
    # opener = urllib.request.build_opener()
    # opener.addheaders = [('User-Agent',
    #                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    # urllib.request.install_opener(opener)

    # calling urlretrieve function to get resource
    try:
        urllib.request.urlretrieve(img_path, filename)
    except OSError:
        urllib.request.urlretrieve(TEMPDIR + '/' + img_path, filename)

    image_PIL = tf.keras.preprocessing.image.load_img(filename,
                                                grayscale=False, color_mode='rgb', target_size=(256,256),
                                                interpolation='nearest')
    image = keras.preprocessing.image.img_to_array(image_PIL,
                                           data_format=None,
                                           dtype=None)
    if model_type == "style":
        image = keras.preprocessing.image.smart_resize(image, (256, 256))
    elif model_type == "rec":
        image = keras.preprocessing.image.smart_resize(image, (224, 224))

    image = tf.expand_dims(image, axis=0, name=None)
    # url = 'http://photographs.500px.com/kyle/09-09-201315-47-571378756077.jpg'
    # file, headers = urllib.urlretrieve(url)
    # # do something
    os.remove(filename)
    return image

def stack_img(img_list, model_type):
    '''
    img_list = {filename: img_path}
    '''
    stacked = []
    for i in img_list:
        for key in i:
            img = load_image(i[key], model_type, key)
            stacked.append(img)
    input_y = np.vstack(stacked)

    return input_y

# img predictor
def predict_image(input_y, model_path):
    model = keras.models.load_model(model_path)
    prediction = model.predict(input_y)
    return prediction

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


if __name__ == "__main__":

    #find stacked vector from multiple images
    input_y = stack_img(img_list)

    #prediction
    prediction = predict_image(input_y, '../../../../../Users/antho/Desktop/linear_back/app/backend/django_app/prediction/mlmodel/models/styleclassifier.h5')
    predictions = pd.DataFrame(prediction, columns=class_names)
    sorted_cats = predictions.sum().sort_values(ascending=False).index
    print('Your prefered style is ' + sorted_cats[0:3][0] + ' with a mix of ' + sorted_cats[0:3][1] + ' and ' + sorted_cats[0:3][2])