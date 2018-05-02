import IP_Functions


def test_IP_Functions():
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
