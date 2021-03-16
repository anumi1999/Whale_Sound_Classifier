# Whale_Sound_Classifier
Whale Sound Classifier is a web based sound classifier that classifies whales on the asis of the audio files that are uploaded by the users. The Classifier is built using **random forest classifier with some parameter hypertuning** and is as of now works for classifying 3 whales - Northen Right Whales, False Killer Whales and Killer Whales. The project is deployed using a flask server.

The starting page of the website is:
![screencapture-localhost-5000-2021-03-16-11_32_58](https://user-images.githubusercontent.com/52823306/111263187-7182d180-864b-11eb-9316-0c00bf6daeef.png)

After uploading the audio the audio waves are sampled and using Machine Learning the whales are being predicted. Here is one of the examples: 
![screencapture-localhost-5000-result-2021-03-16-11_57_17](https://user-images.githubusercontent.com/52823306/111265226-c83dda80-864e-11eb-83a2-7fbceaa5e189.png)

## Demo
Here is an audio file. Note that this is mp4 format file. FOr the website .wav files are to be used strictly.
https://user-images.githubusercontent.com/52823306/111274308-dd206b00-865a-11eb-81fa-31f965532e4b.mp4


The result after uploading this file into the server is:
![screencapture-localhost-5000-result-2021-03-16-13_33_14](https://user-images.githubusercontent.com/52823306/111275520-3c32af80-865c-11eb-8c66-6ef703506d87.png)

## Future Scope
This Whale Sound Classifier can be extended for other sea animals and for other species of whales. 
This project can also be used as a sound classifier for voice recognations. Its only the database on which the model is trained and sampled. 

## Industrial Uses
The industrial aspect of this classifier are:
1. This can be helpful in research base for the whales.
2. The model with some twicks can be used for a voice recognation system.

