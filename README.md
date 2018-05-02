# ImageProcessorS18
BME 590 Final Project

## Overview
This service allows a user to upload an image or batch of images and perform image processing on them.  The user uses the front end interface to upload the files and choose their desired processing steps.  The original images, processed images, associated metadata, and user metrics are stored in a database.  The processed images and associated metadata are displayed on the front end after processing, along with the user’s metrics.  The images are available for download in multiple formats.

### Documentation
Documentation for the service is available at 

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
The number of workers can be modified as desired, or ```workers 4``` can be removed for launch with just one worker.
