# BlueIris-SmartDetection
Python Script to Execute in BlueIris that submits triggered images to Google's AutoML Vision Classification cloud service and Sighthound's Vehicle Recognition service. Also with Pushbullet support. You can easily modify this script to detect people. I also have trained AutoML to detect people in my front door (FrontDoor.py) with only about 50 person images and 50 no person images. Sighthound's People Detection may or may not give you lots of false positives (it does in my experience).

Excuse the mess of code, I am not a coder at all. I just mashed stuff together and kept executing it until it worked.

I've commented where I can so it makes sense (because it is messy, and it's just made to my particular use case).

I have BlueIris execute this python script on a trigger. It does various things such as send me a Pushbullet notification with the image, and execute an HTTP request (in my case a Smartthings action in my smarthome).

I have trained AutoML Vision Image Classification to a bunch of different scenarios in my driveway from months of trigger images (such as "Me arriving" "Wife arriving" "Inlaws arriving" "Me leaving" "Wife leaving" "Unknown car" "Mailman" "Nothing"). 

I have probably anywhere from 20 to 80 images for either category to train the dataset. It's very easy to do all via a GUI, and the average user will never encounter any billing from this small use, if you do, it might be cents.

If "Unknown Car" is the returned variable, then I pass it along to Sighthound to send me a Pusbullet notification me the Make, Model, Colour and Plate (if applicable) of the car detected. Maybe 5% of the time, something slips through that is not a car at all and just vision error.

## Instructions

1) Copy all the scripts to your Users\User Directory
2) Configure the global variables (most of them are at the top), namely you will need a Sighthound Cloud Developer Account Token, and Pushbullet Token, as well as the relevant information from Google's AutoML Vision Classification
3) Namely the one thing that is pretty specific to me, is the image cropping in Sighthound (I had to remove the section of the image that contains a street, otherwise it will just pick off any car that could potentially be driving by). You will probably have to delete that, and replace line 32 in sighthound.py to local_image_path

Please feel free to contribute. God knows this could probably use some refining.
