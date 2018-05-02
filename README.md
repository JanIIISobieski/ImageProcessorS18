# ImageProcessorS18
BME 590 Final Project

## Overview
This service allows a user to upload an image or batch of images and perform image processing on them.  The user uses the front end interface to upload the files and choose their desired processing steps.  The original images, processed images, associated metadata, and user metrics are stored in a database.  The processed images and associated metadata are displayed on the front end after processing, along with the user’s metrics.  The images are available for download in multiple formats.

### Demonstration
[See here for the demonstration video](https://drive.google.com/open?id=16GJyItGLNCmDgSjQiWnrR_utQV7sOkgy).
It covers the performance at the point of submission.

### Documentation
Documentation for the service is available [here](http://image-processor-final-project.readthedocs.io/en/latest/).

## Use
The service can be accessed at [this link](http://vcm-3602.vm.duke.edu:3000).
The user can only import images in PNG, JPEG, or TIFF format, or the user may upload a ZIP archive containing images in one of these formats.
A valid ID tag (any string) must be provided to the User ID space and images must be uploaded or no processing request can be sent.
Up to four functions can be selected. The order in which they are performed on the image is in the order in which they are
arranged. Therefore, Histogram Equalization will always be performed before Contrast Stretch, which will be performed before Log
compression, which will be performed before Reverse Video. Color images will be converted to grayscale before any
processing takes place.
Once the request is sent and the response is received, the processed images should render, along with their histograms,
which are themselves images (.jpeg images of a matplotlib graphing of the pixel intensities).
Images can be downloaded using the button prompt and selecting type. If multiple images are to be downloaded, then a ZIP archive
will be the download type containing images of the proper format. If only a single image was uploaded, a single image will be downloaded.

#### Bug
Unfortunately, a bug exists in the program in that the base64 encoded strings are not able to be rendered by the front
end.
The strings look right upon inspection - they contain a valid header followed by the data - but they are not
rendered by the `<img src={base_64_encoded_string}>` command. Resolving this bug would allow for successful rendering of
the images. This bug persists as well into the download, where the sent base64 encoded string cannot be read by the
download function for download. As such, this bug is critical towards successful performance of the server. However,
communication with the server is pretty successful as a whole.

## Setup
Each component of the service needs to be properly configured in order for it to run properly.  To begin configuration, install all required packages listed in requirements.txt.
### Database
Create a MongoDB database with the command
```
sudo docker run -v $PWD/db:/data/db -p 27017:27017 mongo
```
Ensure that the working directory contains a subdirectory named "imstore".

### Server
To setup the web server, ensure that the working directory contains the files webserver.py, IP_Functions.py, and apifunctions.py.  Launch the server using Gunicorn with the command
```
gunicorn --bind 0.0.0.0:5000 --workers 4 webserver:app
```
The number of workers can be modified as desired, or ```--workers 4``` can be removed for launch with just one worker.
