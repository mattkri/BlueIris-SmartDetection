from google.cloud import automl_v1beta1 as automl
import os
import glob
from google.oauth2 import service_account
import urllib.request
import urllib.parse
import pickle
import json
import requests
from PIL import Image
import base64
import http.client
import ssl
from pushbullet import pushbullet
from sighthound import sighthound
from automl import visionclassification

# For BlueIris I have to run this from the %/Users/Username directory for some reason to execute correctly
# Create a blank file called data.pickle and prediction.pickle (for Sighthound and AutoML respectively), I'm too dumb to figure out how to create the file via Python
avoid_duplicate = "True" # Conditional Argument For AutoML Function to Avoid Giving the same result twice (for example, a parked car in the driveway)
token = "o.xxxxxxxxxxxxxxxxxxxx" # Pushbullet Token
recipient = "" # Pushbullet Device Identifier. Not used currently, so instead it sends it to all devices with Pushbullet installed

project_id = 'project_id' # AutoML Project_id
model_id = 'model_id' # AutoML model_id
min_confidence_score = 0.71 # Cut off for confidence score to be considered relevant

list_of_files = glob.glob('H:\BlueIris\Alerts\*.jpg') # Replace with your Alert Images Directory
local_image_path = max(list_of_files, key=os.path.getctime)
print(local_image_path)

# Use AutoML.py function visionclassification
prediction = visionclassification(local_image_path, project_id, model_id, min_confidence_score, avoid_duplicate)

# Various IF Conditions you can copy paste depending on what you have trained AutoML

if prediction == "Bob Arriving":
 #contents = urllib.request.urlopen("http://url.com").read() #make an HTTP request for IFTTT or WebCoRE
 print("True: Bob is arriving")
 #pushbullet(prediction, token, local_image_path)
 
if prediction == "Alice Arriving":
 print("True: Alice is arriving")
 #contents = urllib.request.urlopen("http://url.com").read()
 #pushbullet(prediction, token, local_image_path)

# If Nothing is Detected or Other Car, run it against Sighthound's AI 
if prediction == "Nothing" or prediction == "Other Car":
 vehicle_detected_return = sighthound(local_image_path)
 if vehicle_detected_return is not None:
  #pushbullet(vehicle_detected_return, token, local_image_path)
  print(vehicle_detected_return)
  # Optionally below, is how I have formatted the script to pass an argument to WebCoRE so it can read it aloud on my Google Cast Devices with cast-web
  
  #vehicle_detected_speak = "Attention. There is a %s in the driveway" % vehicle_detected_return
  #contents = urllib.request.urlopen("http://smartthings.com" % urllib.parse.quote(vehicle_detected_speak)).read()
