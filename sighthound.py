import pickle
import json
import requests
from PIL import Image
import base64
import http.client
import ssl
import urllib.request
import urllib.parse
import os
import glob

def sighthound(local_image_path):
 sighthound_token = "insert-token-here" # Sighthound Token
 plate = ""
 vehicle_detected = ""
 # Comment or Delete the Below of not needed to crop image (to ignore other vehicles on a road, etc.)
 crop_image_location = "crop-image-directory-here" # Needed if cropping image
 im = Image.open(local_image_path)
 width = im.size[0]
 height = im.size[1]
 im2 = im.crop(
  (
   width - 1920,
   height - 950,
   width,
   height
   )
  )
 im2.save(crop_image_location) # Delete until here if not needed to crop
 headers = {"Content-type": "application/json", "X-Access-Token": sighthound_token}
 image_data = base64.b64encode(open(crop_image_location, 'rb').read()) # Change crop_image_location to local_image_path if removing cropped image
 params = json.dumps({"image": image_data.decode('ascii')})
 conn = http.client.HTTPSConnection("dev.sighthoundapi.com", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
 conn.request("POST", "/v1/recognition?objectType=vehicle,licenseplate", params, headers)

# Parse the response and print the make and model for each vehicle found
 response = conn.getresponse()
 results = json.loads(response.read())
 for obj in results["objects"]:
     if obj["objectType"] == "vehicle":
      make  = obj["vehicleAnnotation"]["attributes"]["system"]["make"]["name"]
      model = obj["vehicleAnnotation"]["attributes"]["system"]["model"]["name"]
      color = obj["vehicleAnnotation"]["attributes"]["system"]["color"]["name"]
     if "licenseplate" in obj["vehicleAnnotation"]:
	     plate = obj["vehicleAnnotation"]["licenseplate"]["attributes"]["system"]["string"]["name"]
     vehicle_detected = "%s %s %s %s" % (color, make, model, plate)
     print("Detected: %s %s %s %s" % (color, make, model, plate))
     current_data = {
      'make' : (make),
      'model' : (model),
      'color' : (color)
     }

     try:
      with open('data.pickle', 'rb') as f: # Using Pickle to make sure to not send duplicate notifications
       previous_data = pickle.load(f)

      if current_data == previous_data:
       print('Data is the same!') # If it it's the same, exit
       raise SystemExit
      with open('data.pickle', 'wb') as f:
       pickle.dump(current_data, f, pickle.HIGHEST_PROTOCOL)
     except EOFError:
      with open('data.pickle', 'wb') as f:
       pickle.dump(current_data, f, pickle.HIGHEST_PROTOCOL)
     except FileNotFoundError:
      os.open("prediction.pickle", os.O_CREAT | os.O_EXCL)
 if vehicle_detected != "":
  return vehicle_detected;
