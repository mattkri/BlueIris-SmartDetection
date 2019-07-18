# BlueIris-SmartDetection
Python Script to Execute in BlueIris that submits triggered images to Google's AutoML Vision Classification cloud service and Sighthound's Vehicle Recognition service. Also with Pushbullet support.


Excuse the mess of code, I am not a coder at all. I just mashed stuff together and kept executing it until it worked.

I've commented where I can so it makes sense (because it is messy, and it's just made to my particular use case).

I have BlueIris execute this python script on a trigger. It does various things such as send me a Pushbullet notification with the image, and execute an HTTP request (in my case a Smartthings action in my smarthome).

I have trained AutoML Vision Image Classification to a bunch of different scenarios in my driveway from months of trigger images (such as "Me arriving" "Wife arriving" "Inlaws arriving" "Me leaving" "Wife leaving" "Unknown car" "Mailman" "Nothing"). 

I have probably anywhere from 20 to 80 images for either category to train the dataset. It's very easy to do all via a GUI, and the average user will never encounter any billing from this small use, if you do, it might be cents.

If "Unknown Car" is the returned variable, then I pass it along to Sighthound to send me a Pusbullet notification me the Make, Model, Colour and Plate (if applicable) of the car detected. Maybe 5% of the time, something slips through that is not a car at all and just vision error.

Please feel free to contribute. God knows this could probably use some refining.
