import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
# Access temporary files
import tempfile
from PIL import Image
import numpy as np
import urllib

# Kmeans Color Palette
import faiss
from skimage import color
import tensorflow as tf

# fake visitor to overcome denied request
# Adding information about user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# img loader
def load_image(img_path, filename="temp.jpg"):
    """downloads web image to tempfile and convert into tensor

    Args:
        img_path (str): url to web image
        filename (str, optional): name of the local saved file. Defaults to "temp.jpg".

    Returns:
        image (tensor): expanded image tensor
    """
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
    """loads web image from an input list and outputs list of tensors for downstream models

    Args:
        img_list (list): list of urls to web images

    Returns:
        input_y (tensor): stacked img tensors for feature extraction and classification
        rgb_list (list): list of rgb values for Kmeans clustering
        hex_list (list): list of rgb values for Kmeans clustering
    """
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

def faiss_kmeans(img_path, filename="temp.jpg", n_clusters=4):
    """Using Facebook FAISS library for faster K-Means clustering computation of HSL values from the input images.

    Args:
        img_list (list): list of urls to web images
        filename: If single input image.
        n_clusters: By default we set 4 clusters but can be changed

    Returns:
        faiss_rgb_centers (list): Processed and converted the centers of these clusters to RGB values.
    """

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
                                       k=n_clusters)
    kmeans.train(hsv_pixels.astype(np.float32))
    cluster_centers_ = kmeans.centroids

    # Sort
    faiss_hsv_centers = np.sort(cluster_centers_, axis=0)

    faiss_rgb_centers = color.hsv2rgb(faiss_hsv_centers)

    return faiss_rgb_centers