# FaceTrackingSecurity

With a simple webcam, your program will be able to recognize the faces of people you choose to allow into the system. It will trigger a text, email, and snapshot image alert system, if any unrecognized faces appear in front of your webcam. We’ll also use Cloudinary and PubNub to build a React Native application that can receive a snapshot image of an “intruder’s” face. It will also allow a user to be added to the system if you desire.

# How To Run

1.) In your terminal run the command `npm i` 

2.) Enter the command `pip install opencv-python`

3.) cd into the "client" directory and run the command `npm i` then  `react-native link` (assuming you have the React Native CLI already)

4.) Enter the command `pip install 'pubnub>=4.1.4'`

5.) Get your PubNub API key by clicking the link below and enter the Pub/Sub keys into facetracking.py

 <a href="https://dashboard.pubnub.com/signup?devrel_gh=Cakhavan/PubNubStateMachine">
    <img alt="PubNub Signup" src="https://i.imgur.com/og5DDjf.png" width=260 height=97/>
</a>

6.) Sign up for a free cloudinary account to get your API credentials and enter the command `export CLOUDINARY_URL=cloudinary://API-Key:API-Secret@Cloud-name` with those credentials

7.) Enter the Command `pip install cloudinary`

8.) Sign up for a free ClickSend account and Sendgrid account to get your API credentials

9.) Create a PubNub ClickSend Function and a Sendgrid function and fill in those API credentials

10.) Open another terminal and cd into the `client` directory and do react-native run-ios (assuming you have Xcode iphone simulator already setup).

11.) Run the python script with `python facetracking.py`
