from skimage import exposure
import numpy as np
from scipy import misc
import base64
import os
import shutil
import math
import zipfile
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


def histo(image, case):
    """
       Returns base 64 encoded jpg image of histogram plot for image
       :param image: an ndarray for a single-layer greyscale image,
       where each element corresponds to a pixel.
       :return: A base64 encoded jpg image of histogram plot
       """
    plt.clf()
    H, bins = np.histogram(image, bins='auto', density=True)
    plt.bar(bins[:-1], H, width=1)
    if case == 1:
        plt.title('Histogram of Processed Image')
    else:
        plt.title('Histogram of Original Image')
    plt.xlabel('Value')
    plt.ylabel('Density')

    if case == 1:
        plt.savefig('Histo_Post.jpg')
        histogram = encode_image_string('Histo_Post.jpg')
        os.remove('Histo_Post.jpg')
    else:
        plt.savefig('Histo_Pre.jpg')
        histogram = encode_image_string('Histo_Pre.jpg')
        os.remove('Histo_Pre.jpg')

    return (histogram)


def encode_image_string(filename):
    """
    Returns the base64 encoded string for an image file
    :param filename: image file to base64 encode
    :return: base64 string for image
    """
    with open(filename, "rb") as image_file:
        image_string = base64.b64encode(image_file.read())
        return image_string


def decode_image_string(image_string):
    """
    Creates a png image file of base64 encoded string
    :param image_string: base64 encoded string of image
    :return: Creates a png image file of encoded string
    """
    imgdata = base64.b64decode(image_string)
    filename = 'image'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return


def unpack_zip(zip_string):
    """
    Creates an array of base64 encoded image strings
     from a base64 encoded zip file
    :param zip_string: A base64 encoded zip file
    that contains images
    :return: An array of base64 encoded strings
    corresponding to each image
    """
    decoded = base64.b64decode(zip_string)
    if os.path.exists('strings.zip'):
        os.remove('strings.zip')
    filename = 'strings.zip'
    with open(filename, 'wb') as f:
        f.write(decoded)

    if os.path.exists('images'):
        shutil.rmtree('images')
    zip_ref = zipfile.ZipFile('strings.zip', 'r')
    zip_ref.extractall('images')
    zip_ref.close()

    image_strings = []
    for filename in os.listdir('images'):
        imstring = encode_image_string('images/'+filename)
        image_strings.append(imstring)

    os.remove('strings.zip')
    shutil.rmtree('images')

    return image_strings


def return_image_strings(b64_array):
    """
    Returns an array of b64 encoded image strings, without headers,
    from 1 of 2 inputs.  Either an array of base64 encoded
    strings or a base64 encoded zipfile.
    :param b64_array: an array of base64 strings
    :return: an array of b64 encoded image strings.
    """

    if b64_array[0][0:10] == "data:image":
        for idx, val in enumerate(b64_array):
            marker = val.find("base64,")
            b64_array[idx] = val[marker+7:]
        return b64_array
    else:
        marker = b64_array[0].find("base64,")
        b64_array[0] = b64_array[0][marker+7:]
        return unpack_zip(b64_array)


def resave_image(image_strings, ftype):

    """
    Returns a base64 encoding of a single image or
    zipfile of images, with a header, that are saved as a
    specified file type
    :param image_strings: An array of base64 encoded image strings
    :param ftype: A string that specifies what filetype the user wants
     the files saved as (jpg, tiff, png...)
    :return: base64 encoded zip archive of images or a
    single base64 encoded image
    """

    if len(image_strings) == 1:
        decode_image_string(image_strings[0])
        img = Image.open('image')
        img.save('image.'+ftype)
        encoded_1 = encode_image_string('image.'+ftype)
        encoded_1 = str(encoded_1)[2:]
        encoded_1 = "data:image/"+ftype+";base64," + str(encoded_1)
        os.remove('image')
        os.remove('image.'+ftype)
        return encoded_1
    else:
        if os.path.exists("tmp1"):
            shutil.rmtree("tmp1")

        os.makedirs("tmp1")
        i = 0

        for x in image_strings:
            try:
                decode_image_string(x)
            except TypeError:
                print('base64 string expected')

            img = Image.open('image')
            img.save('tmp1/image'+str(i)+'.'+ftype)
            os.remove('image')
            i = i + 1

        if os.path.exists("zipped_"+ftype+"_images.zip"):
            os.remove("zipped_"+ftype+"_images.zip")
        shutil.make_archive("zipped_"+ftype+"_images", 'zip', "tmp1")

        with open("zipped_"+ftype+"_images.zip", 'rb') as f:
            bytes = f.read()
            encoded = base64.b64encode(bytes)

        encoded = str(encoded)[2:]
        encoded = "data:application/zip;base64," + str(encoded)
        shutil.rmtree("tmp1")
        os.remove("zipped_"+ftype+"_images.zip")

        return encoded


def add_header(image_string):

    """
    Adds the base64 encoding header for jpg images
    to a base64 encoded string
    :param image_string: A base64 encoded image string
    without a header
    :return: A base64 encoded string with a jpg header
    """
    image_string = str(image_string)[2:]
    image_string_with_head = "data:image/jpeg;base64,"+str(image_string)
    return (image_string_with_head)


def run_process(image_string, filters):

    """
       Runs selected filters on input image
       :param image_string: base64 encoding of image file
       :param filters: an array that corresponds to
       what filters the user selected
       :raises TypeError: If image input is not an image file
       :raises TypeError: If image_string is not a base64 string
       :return image_filt_string: A base64 encoding of the filtered jpg image
       :return image_prefilt_string: A base64 encoding of greyscale, input jpg image
       :return im_size: A tuple with dimensions of input image
       :return histo_pre: The histogram arrays for the image pre-processing
       :return histo_post: The histogram arrays for the image post-processing
       """

    try:
        decode_image_string(image_string)
    except TypeError:
        print('base64 string expected')

    try:
        im_array = misc.imread('image', flatten=True)
        os.remove('image')
    except TypeError:
        print('Image file expected')

    misc.imsave('prefilt.jpg', im_array)
    image_prefilt_string = encode_image_string('prefilt.jpg')
    os.remove('prefilt.jpg')

    histo_pre = histo(im_array, 0)
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
    histo_post = histo(image_filt, 1)

    misc.imsave('postfilt.jpg', image_filt)
    image_filt_string = encode_image_string('postfilt.jpg')
    os.remove('postfilt.jpg')

    return image_filt_string, image_prefilt_string, im_size, histo_pre, histo_post


def main():
    imstring = encode_image_string('lion.jpg')
    imstring2 = encode_image_string('lion.jpg')

    zip_string = resave_image([imstring, imstring2], "tiff")
    image_strings = unpack_zip(zip_string)
    decode_image_string(image_strings[0])
    post, pre, im_size, histopre, histopost = run_process(imstring, [0,0,1,0])


if __name__ == "__main__":
    main()
