import IP_Functions
from scipy import misc
import base64


def test_ip_functions():
    imstring = IP_Functions.encode_image_string('lion.jpg')
    post, pre, im_size, histopre, histopost = \
        IP_Functions.run_process(imstring, [1, 0, 0, 0])
    assert im_size == (1080, 1920)
    encoded_zip = IP_Functions.resave_image([imstring, imstring], "jpg")
    encoded_zip1 = str(encoded_zip)[28:]
    string_array = IP_Functions.unpack_zip(encoded_zip1)
    post1, pre1, im_size1, histopre1, histopost1 =\
        IP_Functions.run_process(string_array[0], [1, 0, 0, 0])
    assert im_size1 == (1080, 1920)

    im_array = misc.imread('lion.jpg', flatten=True)
    image_he = IP_Functions.histo_equal(im_array)
    image_cs = IP_Functions.contrast_stretch(im_array)
    image_log = IP_Functions.log_compression(im_array)
    inverted = IP_Functions.rev_vid(im_array)

    histo_pre = IP_Functions.histo(im_array, 0)
    imgdata = base64.b64decode(histo_pre)
    filename = 'histo_pre.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    misc.imsave('histo_equal_image.jpg', image_he)
    histo_post = IP_Functions.histo(image_he, 1)
    imgdata = base64.b64decode(histo_post)
    filename = 'histogram_histoeq.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    misc.imsave('contrast_stretch_image.jpg', image_cs)
    histo_post = IP_Functions.histo(image_cs, 1)
    imgdata = base64.b64decode(histo_post)
    filename = 'histogram_contrast_stretch.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    misc.imsave('log_compressed.jpg', image_log)
    histo_post = IP_Functions.histo(image_log, 1)
    imgdata = base64.b64decode(histo_post)
    filename = 'histogram_log_compress.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    misc.imsave('rev_vid.jpg', inverted)
    histo_post = IP_Functions.histo(inverted, 1)
    imgdata = base64.b64decode(histo_post)
    filename = 'histogram_inverted.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
