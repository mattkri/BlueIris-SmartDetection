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

def visionclassification(local_image_path, project_id, model_id, min_confidence_score, avoid_duplicate="False"):
 os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="file.json" # You need to generate and download a json key in AutoML, you only need one if you keep datasets in one project
 compute_region = 'us-central1' # This is by default
 prediction = ""
 automl_client = automl.AutoMlClient()

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
     if result.classification.score > min_confidence_score:
      prediction = result.display_name
     if avoid_duplicate == "True":
      try:
       with open('prediction.pickle', 'rb') as f:
        previous_prediction = pickle.load(f)

       if result.display_name == previous_prediction:
        print('Data is the same!')
        raise SystemExit
       with open('prediction.pickle', 'wb') as f:
        pickle.dump(result.display_name, f, pickle.HIGHEST_PROTOCOL)
      except EOFError:
       with open('prediction.pickle', 'wb') as f:
        pickle.dump(result.display_name, f, pickle.HIGHEST_PROTOCOL)
      except FileNotFoundError:
       os.open("prediction.pickle", os.O_CREAT | os.O_EXCL)
 return prediction;
