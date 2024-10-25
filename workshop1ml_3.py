#!/usr/bin/env python
# coding: utf-8

import os
import cv2
import boto3
from cvzone.HandTrackingModule import HandDetector

# Initialize camera capture and AWS EC2 resource
cap = cv2.VideoCapture(0)
ec2 = boto3.resource("ec2")

# List to store IDs of launched EC2 instances
allOS = []

# Initialize hand detector (detects 1 hand at a time)
detector = HandDetector(maxHands=1)

def myOSLaunch():
    """
    Function to launch a new EC2 instance using the specified AMI and instance type.
    """
    instances = ec2.create_instances(
        ImageId="ami-0a2acf24c0d86e927",  # Use your preferred AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=["sg-0042ea78f2f411484"]  # Replace with your security group ID
    )
    # Add the launched instance ID to the list
    myid = instances[0].id
    allOS.append(myid)
    print("Total EC2 instances running:", len(allOS))
    print("Launched Instance ID:", myid)

def osTerminate():
    """
    Function to terminate the last launched EC2 instance.
    """
    if allOS:
        osdelete = allOS.pop()  # Get the last instance ID from the list
        ec2.instances.filter(InstanceIds=[osdelete]).terminate()
        print(f"Terminated Instance ID: {osdelete}")
    else:
        print("No instances to terminate.")

while True:
    # Capture frame from webcam
    status, photo = cap.read()
    
    # Detect hand and check the status
    hand = detector.findHands(photo, draw=False)

    if hand:
        lmlist = hand[0]
        totalFingers = detector.fingersUp(lmlist)

        # Check specific hand gestures to trigger AWS EC2 operations
        if totalFingers == [0, 1, 1, 0, 0]:
            print("2 and 3 fingers are up")
            myOSLaunch()  # Launch EC2 instance

        elif totalFingers == [0, 1, 0, 0, 0]:
            print("Index finger is up")
            osTerminate()  # Terminate EC2 instance

        else:
            print("Perform a valid gesture")

    # Display the current video frame
    cv2.imshow("Gesture Control", photo)

    # Close the window when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()














