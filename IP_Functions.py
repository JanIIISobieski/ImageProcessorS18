from skimage import data, img_as_float, io
from skimage import exposure
import numpy as np
from scipy import misc

def histo_equal(image):

    image_he = exposure.equalize_hist(image)

    return image_he

def contrast_stretch(image):

    p2, p98 = np.percentile(image, (2, 98))
    image_cs = exposure.rescale_intensity(image, in_range=(p2, p98))

    return image_cs

def log_compression(image):

    image_log = np.log(image)

    return(image_log)

def rev_vid(image):

    inverted = np.invert(image, dtype=float32)

    return(inverted)

def image_size(image):

    size = np.shape(image)

    return(size)

def histo(image):

    histogram = np.histogram(image, bins = 100)

    return (histogram)


def run_process(image, filters):

    #im_array = io.imread(image, as_grey=True)
    im_array = misc.imread(image, flatten=True)

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

    return(image_filt, im_size, histo_pre, histo_post)