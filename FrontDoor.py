import base64
import json
import os
import ssl
import glob
import urllib.request
from automl import visionclassification
from pushbullet import pushbullet
      
project_id = 'project-id' # AutoML Project_id
model_id = 'model-id' # AutoML model_id
min_confidence_score = 0.71
token = "o.xxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Pushbullet Token

list_of_files = glob.glob('H:\BlueIris\FrontDoor\*.jpg') # Replace with your directory of Alert Images
local_image_path = max(list_of_files, key=os.path.getctime)
print(local_image_path)

prediction = visionclassification(local_image_path, project_id, model_id, min_confidence_score)

print(prediction)

# Copy Paste depending on the classifications you create

if prediction == "Person":
 #contents = urllib.request.urlopen("http://url.com").read() #Makes a Web Request depending on outcome
 print(contents)
 #pushbullet(prediction, token, local_image_path) #Uncomment to send pushbullet notification

