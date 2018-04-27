from skimage import exposure
import numpy as np
from scipy import misc
import base64
import imageio
import os
import shutil
import math
from PIL import Image
import matplotlib.pyplot as plt

def histo_equal(image):
    """
    Performs histogram equalization on input image.
    :param image: an ndarray for a single-layer greyscale image,
    where each element corresponds to a pixel.
    :return: A histogram equalized ndarray
    """

    image_he = exposure.equalize_hist(image)
    image_he = image_he * (np.amax(image) - np.amin(image)) + np.amin(image)

    return image_he

def contrast_stretch(image):
    """
    Performs contrast stretching on input image
    :param image: an ndarray for a single-layer greyscale image,
    where each element corresponds to a pixel.
    :return: A contrast stretched ndarray
    """

    p2, p98 = np.percentile(image, (5, 95))
    image_cs = exposure.rescale_intensity(image, in_range=(p2, p98))
    image_cs = image_cs * (np.amax(image) - np.amin(image)) + np.amin(image)

    return (image_cs)

def log_compression(image):
    """
       Performs log compression on input image
       :param image: an ndarray for a single-layer greyscale image,
       where each element corresponds to a pixel.
       :return: A log-compressed ndarray
       """

    c = 255 / math.log(1+np.amax(image))
    image_log = c*np.log(image + 1)

    return(image_log)

def rev_vid(image):
    """
       Performs reverse video filter on input image
       :param image: an ndarray for a single-layer greyscale image,
       where each element corresponds to a pixel.
       :return: An ndarray that is the reverse video of input
       """
    inverted = 255 - image

    return(inverted)

def image_size(image):
    """
       Returns image dimensions of input
       :param image: an ndarray for a single-layer greyscale image,
       where each element corresponds to a pixel.
       :return: Tuple of array dimensions
       """

    size = np.shape(image)

    return(size)

def histo(image):
    """
       Finds histogram of intensities in input image
       :param image: an ndarray for a single-layer greyscale image,
       where each element corresponds to a pixel.
       :return: A list of 2 arrays where the first is the normalized number
        of pixels in an intensity range, and the second is the bins
        of intensity ranges.
       """

    histogram = np.histogram(image, bins='auto', density=True)

    return (histogram)


def encode_image_string(filename):
    """
    Returns the base64 encoded string for an image file
    :param filename: Name of image file to base64 encode
    :return: base64 string for image
    """
    with open(filename, "rb") as image_file:
        image_string = base64.b64encode(image_file.read())
        return image_string

def decode_image_string(image_string):
    """
    Creates a png image file of base64 encoded string
    :param image_string: base64 encoded string for image
    :return: Creates a png image file of encoded string
    """
    imgdata = base64.b64decode(image_string)
    filename = 'image.png'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return


def resave_image(image_strings, ftype):

    os.makedirs("/tmp")
    i = 0
    for x in image_strings:
        try:
            image = decode_image_string(x)
        except TypeError:
            print('base64 string expected')

        imageio.imwrite('/tmp/temp'+str(i)+'.'+ftype, image)
        i = i + 1

    shutil.make_archive("zipped_"+ftype+"_images", 'zip', "/tmp")

    with open("zipped_"+ftype+"_images.zip", 'rb') as fin, open("zipped_"+ftype+"_images.zip.b64", 'w') as fout:
        base64.encode(fin, fout)

    return

def run_process(image_string, filters):

    """
       Runs selected filters on input image
       :param image_string: base64 encoding of image file
       :param filters: an array that corresponds to
       what filters the user selected
       :raises TypeError: If image input is not an image file
       :raises TypeError: If image_string is not a base64 string
       :return image_filt_string: A base64 encoding of the final filtered image
       :return image_prefilt_sgring: A base64 encoding of greyscale, input image
       :return im_size: A tuple with dimensions of input image
       :return histo_pre: The histogram arrays for the image pre-processing
       :return histo_post: The histogram arrays for the image post-processing
       """

    try:
        decode_image_string(image_string)
    except TypeError:
        print('base64 string expected')

    try:
        im_array = misc.imread('image.png', flatten=True)
        os.remove('image.png')
    except TypeError:
        print('Image file expected')


    misc.imsave('prefilt.jpg', im_array)
    image_prefilt_string = encode_image_string('prefilt.jpg')
    os.remove('prefilt.jpg')

    histo_pre = histo(im_array)
    im_size = image_size(im_array)

    if filters[0] == 1:
        im_array = histo_equal(im_array)
    if filters[1] == 1:
        im_array = contrast_stretch(im_array)
    if filters[2] == 1:
        im_array = log_compression(im_array)
    if filters[3] == 1:
        im_array = rev_vid(im_array)

    image_filt = im_array
    histo_post = histo(image_filt)

    misc.imsave('postfilt.jpg', image_filt)
    image_filt_string = encode_image_string('postfilt.jpg')
    os.remove('postfilt.jpg')

    return image_filt_string, image_prefilt_string, im_size, histo_pre, histo_post


def main():
    imstring = encode_image_string("lion.jpg")
    run_process(imstring, [1,0,0,0])

if __name__ == "__main__":
    main()