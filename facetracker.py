import face_recognition # Machine Learning Library for Face Recognition
import cv2 # OpenCV
import numpy as np # Handling data
import time
import os,sys

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNOperationType, PNStatusCategory

# PubNub Config
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "YOUR SUBSCRIBE KEY"
pnconfig.publish_key = "YOUR PUBLISH KEY"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)

from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# Cloudinary Config
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    exec(open('settings.py').read())
DEFAULT_TAG = "python_sample_basic"

# Setup some Global Variables
video_capture = cv2.VideoCapture(0) # Webcam instance
known_face_names = [] # Names of faces
known_face_encodings = [] # Encodings of Faces
count = 0 # Counter for Number of Unknown Users
flag = 0 # Flag for Setting/Unsetting "Intruder Mode"

def sendAlerts():
    dictionary = {
    "to" : 'RECEIVING PHONE NUMBER',
    "body": "There is an unregistered user at your desk!"
    }
    pubnub.publish().channel('clicksend-text').message(dictionary).pn_async(publish_callback)

    dictionary = {
    "to": "EMAIL RECEIVER",
    "toname": "EMAIL SENDER",
    "subject": "INTRUDER ALERT",
    "text": "THERE IS AN UNREGISTERED USER AT YOUR DESK"
    }   
    pubnub.publish().channel('email-sendgrid-channel').message(dictionary).pn_async(publish_callback)
   
def upload_files(msg):
    global count
    response = upload(msg, tags=DEFAULT_TAG) # Upload Image to Cloudinary
    url, options = cloudinary_url( #
        response['public_id'],
        format=response['format'],
        width=200,
        height=150,
        crop="fill"
    )
    dictionary = {"url": url, "ID": count}
    pubnub.publish().channel('global').message(dictionary).pn_async(publish_callback)
    count+=1

def publish_callback(result, status):
    pass
    # Handle PNPublishResult and PNStatus

def addUser(ID, name):
    global known_face_encodings, known_face_names, flag
    path = './Unknown_User' + str(ID) # Append User ID to File Path
    # Load User's picture and learn how to recognize it.
    user_image = face_recognition.load_image_file('% s.jpg' % (path)) # Load Image
    user_face_encoding = face_recognition.face_encodings(user_image)[0] # Encode Image
    known_face_encodings.append(user_face_encoding) # Add Encoded Image to 'Known Faces' Array
    known_face_names.append(name) # Append New User's Name to Database
    flag = 0 # Reset Unknown User Flag

def Alert():
    global count
    video_capture = cv2.VideoCapture(0) # Create Open CV Webcam Instance
    path = './' # Specify where you want the snapshot to be stored
    name = 'Unknown_User' + str(count) # Append User ID to File Path

    # Wait for 3 seconds
    print('Taking picture in 3')
    time.sleep(1)
    print('Taking picture in 2')
    time.sleep(1)
    print('Taking picture in 1')
    time.sleep(1)

    # Take Picture
    ret, frame = video_capture.read()

    # Grayscale Image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Save Image in File Path
    status = cv2.imwrite('% s/% s.jpg' % (path, name),gray)
    print('Unknown User Saved to Database', status)

    # Upload Snapshot to Cloudinary 
    upload_files('% s/% s.jpg' % (path,name))

    # Send Out Email and Text Alerts
    sendAlerts()




class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means here
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does not allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type
 
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
    def message(self, pubnub, message):
        addUser(message.message["ID"], message.message["name"])
 
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('ch1').execute()

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("adam.jpeg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("17.png")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]

# Create Names for Sample Face encodings
known_face_names = [
    "adam",
    "dylan"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while(True):
    
    video_capture = cv2.VideoCapture(0)
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # Set Unknown User Flag and Send Alerts
            global flag
            if(name=='Unknown' and flag==0):
                flag = 1
                Alert()


    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
