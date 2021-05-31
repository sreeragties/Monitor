from datetime import datetime

import cv2
import imutils
import numpy as np
import os
from scipy.spatial import distance as dist

from firebase_config import storage, database, user
from socialdistance.mylib import config
from socialdistance.mylib.detection import detect_people
from socialdistance.mylib.mailer import Mailer

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
if config.USE_GPU:
    # set CUDA as the preferable backend and target
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def Camera1():
    print("Entered Camera 1")
    video = cv2.VideoCapture('socialdistance/mylib/videos/test.mp4')
    Camera1.count = 0
    Camera1.now = datetime.now()
    while True:
        print("Processsing Frames 1")

        (grabbed, frame) = video.read()

        # resize the frame and then detect people (and only people) in it
        frame = imutils.resize(frame, width=700)
        results = detect_people(frame, net, ln, personIdx=LABELS.index("person"))

        # initialize the set of indexes that violate the max/min social distance limits
        serious = set()
        abnormal = set()

        # ensure there are *at least* two people detections (required in
        # order to compute our pairwise distance maps)
        if len(results) >= 2:

            # extract all centroids from the results and compute the
            # Euclidean distances between all pairs of the centroids
            centroids = np.array([r[2] for r in results])
            D = dist.cdist(centroids, centroids, metric="euclidean")

            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    # check to see if the distance between any two
                    # centroid pairs is less than the configured number of pixels
                    if D[i, j] < config.MIN_DISTANCE:
                        # update our violation set with the indexes of the centroid pairs
                        serious.add(i)
                        serious.add(j)
                    # update our abnormal set if the centroid distance is below max distance limit
                    if (D[i, j] < config.MAX_DISTANCE) and not serious:
                        abnormal.add(i)
                        abnormal.add(j)

        # loop over the results
        for (i, (prob, bbox, centroid)) in enumerate(results):
            # extract the bounding box and centroid coordinates, then
            # initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)

            # if the index pair exists within the violation/abnormal sets, then update the color
            if i in serious:
                color = (0, 0, 255)
            elif i in abnormal:
                color = (0, 255, 255)  # orange = (0, 165, 255)

            # draw (1) a bounding box around the person and (2) the
            # centroid coordinates of the person,
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 2)

        # draw some of the parameters
        Safe_Distance = "Safe distance: >{} px".format(config.MAX_DISTANCE)
        cv2.putText(frame, Safe_Distance, (470, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)
        Threshold = "Threshold limit: {}".format(config.Threshold)
        cv2.putText(frame, Threshold, (470, frame.shape[0] - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)

        # draw the total number of social distancing violations on the output frame
        text = "Total serious violations: {}".format(len(serious))
        cv2.putText(frame, text, (10, frame.shape[0] - 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 255), 2)

        text1 = "Total abnormal violations: {}".format(len(abnormal))
        cv2.putText(frame, text1, (10, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)

        # ------------------------------Alert function----------------------------------#

        if len(serious) >= config.Threshold:
            if Camera1.count == 0:
                Camera1.now = datetime.now()

            cv2.putText(frame, "-ALERT: Violations over limit-", (10, frame.shape[0] - 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.60, (0, 0, 255), 2)
            if config.ALERT:
                print("")
                print('[INFO] Sending mail...')
                Mailer().send(config.MAIL)
                print('[INFO] Mail sent')

            cur = datetime.now()

            if Camera1.count == 0 or (cur - Camera1.now).total_seconds() > 10:
                Camera1.now = cur
                Camera1.count += 1
                current_time = cur.strftime("_%d_%m_%Y_%H_%M_%S")
                cv2.imwrite("extract/camera_1_frame%s.jpg" % current_time, frame)  # save frame as JPEG file
                path_on_cloud = "camera1/" + current_time + ".jpg"
                storage.child(path_on_cloud).put("extract/camera_1_frame%s.jpg" % current_time)
                url = storage.child(path_on_cloud).get_url(user['idToken'])
                data = {current_time: url}
                database.child("camera1").child(current_time).set(data)
                os.remove("extract/camera_1_frame%s.jpg" % current_time)
                print('Read a new frame: ', frame)

        else:
            Camera1.count = 0

        # config.ALERT = False
        # ------------------------------------------------------------------------------#


def Camera2():
    video = cv2.VideoCapture('socialdistance/mylib/videos/test1.mp4')
    Camera2.count = 0
    Camera2.now = datetime.now()
    while True:
        (grabbed, frame) = video.read()

        # resize the frame and then detect people (and only people) in it
        frame = imutils.resize(frame, width=700)
        results = detect_people(frame, net, ln, personIdx=LABELS.index("person"))

        # initialize the set of indexes that violate the max/min social distance limits
        serious = set()
        abnormal = set()

        # ensure there are *at least* two people detections (required in
        # order to compute our pairwise distance maps)
        if len(results) >= 2:

            # extract all centroids from the results and compute the
            # Euclidean distances between all pairs of the centroids
            centroids = np.array([r[2] for r in results])
            D = dist.cdist(centroids, centroids, metric="euclidean")

            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    # check to see if the distance between any two
                    # centroid pairs is less than the configured number of pixels
                    if D[i, j] < config.MIN_DISTANCE:
                        # update our violation set with the indexes of the centroid pairs
                        serious.add(i)
                        serious.add(j)
                    # update our abnormal set if the centroid distance is below max distance limit
                    if (D[i, j] < config.MAX_DISTANCE) and not serious:
                        abnormal.add(i)
                        abnormal.add(j)

        # loop over the results
        for (i, (prob, bbox, centroid)) in enumerate(results):
            # extract the bounding box and centroid coordinates, then
            # initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)

            # if the index pair exists within the violation/abnormal sets, then update the color
            if i in serious:
                color = (0, 0, 255)
            elif i in abnormal:
                color = (0, 255, 255)  # orange = (0, 165, 255)

            # draw (1) a bounding box around the person and (2) the
            # centroid coordinates of the person,
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 2)

        # draw some of the parameters
        Safe_Distance = "Safe distance: >{} px".format(config.MAX_DISTANCE)
        cv2.putText(frame, Safe_Distance, (470, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)
        Threshold = "Threshold limit: {}".format(config.Threshold)
        cv2.putText(frame, Threshold, (470, frame.shape[0] - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)

        # draw the total number of social distancing violations on the output frame
        text = "Total serious violations: {}".format(len(serious))
        cv2.putText(frame, text, (10, frame.shape[0] - 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 255), 2)

        text1 = "Total abnormal violations: {}".format(len(abnormal))
        cv2.putText(frame, text1, (10, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)

        # ------------------------------Alert function----------------------------------#

        if len(serious) >= config.Threshold:
            if Camera2.count == 0:
                Camera2.now = datetime.now()

            cv2.putText(frame, "-ALERT: Violations over limit-", (10, frame.shape[0] - 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.60, (0, 0, 255), 2)
            if config.ALERT:
                print("")
                print('[INFO] Sending mail...')
                Mailer().send(config.MAIL)
                print('[INFO] Mail sent')

            cur = datetime.now()

            if Camera2.count == 0 or (cur - Camera2.now).total_seconds() > 10:
                Camera2.now = cur
                Camera2.count += 1
                current_time = cur.strftime("_%d_%m_%Y_%H_%M_%S")
                cv2.imwrite("extract/camera_1_frame%s.jpg" % current_time, frame)  # save frame as JPEG file
                path_on_cloud = "camera1/" + current_time + ".jpg"
                storage.child(path_on_cloud).put("extract/camera_1_frame%s.jpg" % current_time)
                url = storage.child(path_on_cloud).get_url(user['idToken'])
                data = {current_time: url}
                database.child("camera1").child(current_time).set(data)
                os.remove("extract/camera_1_frame%s.jpg" % current_time)
                print('Read a new frame: ', frame)

        else:
            Camera2.count = 0

        # config.ALERT = False
        # ------------------------------------------------------------------------------#
