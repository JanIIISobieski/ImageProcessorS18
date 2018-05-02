# Go Gitters Final Project Front End

#Link for demonstration
[See here for the demonstration video](https://drive.google.com/open?id=16GJyItGLNCmDgSjQiWnrR_utQV7sOkgy).
It covers the performance of the point of submission.

# Use
User can only import .png, .jpeg, and .zip archives of images.
A valid ID tag (any string) must be provided to the User ID space, or no processing request can be sent.
Images must also be uploaded otherwise no processing request can be sent either.
Four functions can be selected. The order in which they are performed on the image is in the order in which they are
arranged.
That is, Histogram Equalization will always be performed before Contrast Stretch, which will be performed before Log
compression, which will be performed before Reverse Video. Color images will be converted to greyscale before any
processing takes place.
Once the request is received and then sent back, the processed images should render, as well as their histograms,
which are themselves images (.jpeg images of a matplotlib graphing of the pixel intensities).
Images can be downloaded using the button prompt and selecting type. If multiple images are sent, then a .zip archive
will be the download type. If only a single image was uploaded, a single image will be downloaded.

#Bug
Unfortunately, a bug exists in the program in that the base64 encoded strings are not able to be rendered by the front
end.
It appears that the strings look right upon inspection - contain a valid header followed by the data - but they are not
rendered by the `<img src={base_64_encoded_string}>` command. Resolving this bug would allow for successful rendering of
the images. This bug persists as well into the download, where the sent base64 encoded string cannot be read by the
download function for download. As such, this bug is critical towards successful performance of the server. However,
communication with the server is as a whole pretty successful