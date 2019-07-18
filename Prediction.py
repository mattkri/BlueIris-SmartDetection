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

# For BlueIris I have to run this from the %/Users/Username directory for some reason to execute correctly
# Create a blank file called data.pickle and prediction.pickle (for Sighthound and AutoML respectively)

token = "" # Pushbullet Token in o.xxxxxxxxxxxxxxxxxxx
recipient = "" # Pushbullet Recipient
sighthound_token = "" # Sighthound Token
crop_image_location = "C:\BlueIris\sighthound\driveway2.jpg" # Needed if cropping image
plate = '' # Define as null in case plate isn't returned by Sighthound

# AutoML Variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="FILENAME.json" # You need to generate and download a json key in AutoML
project_id = 'project-id-here' # Required
compute_region = 'us-central1' # This is by default
model_id = 'model-id-here' # Required
prediction = ""

automl_client = automl.AutoMlClient()

list_of_files = glob.glob('C:\BlueIris\Alerts\*.jpg') # Get latest file from BlueIris Directory
local_image_path = max(list_of_files, key=os.path.getctime)
print(local_image_path)

# DEBUG Test Image
#local_image_path = ("C:\\Users\\Username\\test.jpg") ## LEAVE COMMENTED OUT EXCEPT FOR TESTING

## SIGHTHOUND FUNCTION
def sighthound():
 # Comment out or Delete the Below if not needed to crop image (to ignore other vehicles)
 plate = ""
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
     print("Detected: %s %s %s %s" % (color, make, model, plate))
     current_data = {
      'make' : (make),
      'model' : (model),
      'color' : (color)
     }

     with open('data.pickle', 'rb') as f: # Using Pickle to make sure to not send duplicate notifications
      previous_data = pickle.load(f)

     if current_data == previous_data:
      print('Data is the same!') # If it it's the same, exit
      raise SystemExit
     with open('data.pickle', 'wb') as f:
      pickle.dump(current_data, f, pickle.HIGHEST_PROTOCOL)
 vehicle_detected = "%s %s %s %s" % (color, make, model, plate)
 return vehicle_detected;

## PUSHBULLET FUNCTION
def pushbullet (title):
 jpgbase = os.path.basename(local_image_path)
 jpgimg = local_image_path
 res = requests.post("https://api.pushbullet.com/v2/upload-request",
  headers={
   "Access-Token": token,
   "Content-Type": "application/json"
   },
   data=json.dumps({"file_name": jpgbase, "file_type": "image/jpeg"}))
 
 js = json.loads(res.content)
 files = {'file': open(jpgimg, 'rb')}
 requests.post(js['upload_url'], files=files)
 fileurl = js['file_url']
 res = requests.post("https://api.pushbullet.com/v2/pushes",
                    headers={
                        "Access-Token": token,
                        "Content-Type": "application/json"},
                    data=json.dumps({
                        #"device_iden": recipient,
                        "type": "file",
						"title": title,
                        "file_name": jpgbase,
                        "file_type": "image/jpeg",
                        "file_url": fileurl}))



# Get the full path of the model.
model_full_id = automl_client.model_path(project_id, compute_region, model_id)

# Google AutoML Vision - Upload Image and Read Result, Check if the Same
prediction_client = automl.PredictionServiceClient()
with open(local_image_path, 'rb') as f_in:
  image_bytes = f_in.read()
payload = {'image': {'image_bytes': image_bytes}}
result = prediction_client.predict(model_full_id, payload)


for result in result.payload:
    print("Predicted class name: {}".format(result.display_name))
    print("Predicted class score: {}".format(result.classification.score))
    if result.classification.score > 0.71:
     prediction = result.display_name

    with open('prediction.pickle', 'rb') as f:
     previous_prediction = pickle.load(f)

    if result.display_name == previous_prediction:
     print('Data is the same!')
     raise SystemExit
    with open('prediction.pickle', 'wb') as f:
     pickle.dump(result.display_name, f, pickle.HIGHEST_PROTOCOL)
    
if prediction == "Your DisplayName Variable Here":
 contents = urllib.request.urlopen("https://whatever.com").read() # Make an HTTP Request for this condition, whatever suits your uses, like IFTTT or Smartthings Webcore
 #print("True: Whatever")
 pushbullet(prediction) # Send a Pushbullet notification with the image
 
if prediction == "You can just copy paste for various labels":
 #print("True: Whatever")
 contents = urllib.request.urlopen("https://www.whatever.com").read()
 pushbullet(prediction) # Send a Pushbullet notification with the image
 
# In my case, since I have a label in AutoML called Other Car, if this condition is met, send to Sighthound for analysis and return result
if prediction == "" or prediction == "Other Car":
 vehicle_detected_return = sighthound()
 if vehicle_detected_return is not None:
  pushbullet(vehicle_detected_return)
  # The below is an example of another use case of mine, with Smartthings, I have this text cast to the Google Homes in my house using the cast-web plugin for Smartthings and WebCoRE to execute the script
  #vehicle_detected_speak = "Attention. There is a %s in the driveway" % vehicle_detected_return
  #contents = urllib.request.urlopen("https://www.hidden.com" % urllib.parse.quote(vehicle_detected_speak)).read()
