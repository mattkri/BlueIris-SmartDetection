import urllib.request
import urllib.parse
import pickle
import json
import requests
from PIL import Image
import base64
import http.client
import ssl
import os

def pushbullet (title, token, local_image_path):
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