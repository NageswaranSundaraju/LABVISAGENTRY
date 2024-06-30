#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import os
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import time
import threading
import logging

logging.basicConfig(filename='admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def train(progress, estimated_time_label, root):
    # our images are located in the dataset folder
    logging.info("Training starts...")
    print("[INFO] start processing faces...")
    imagePaths = list(paths.list_images("dataset"))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    start_time = time.time()
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

        # Update progress bar
        progress['value'] = (i + 1) / len(imagePaths) * 100
        estimated_time = (time.time() - start_time) / (i + 1) * (len(imagePaths) - (i + 1))
        estimated_time_label.config(text=f"Estimated time left: {int(estimated_time)} seconds")

        root.update_idletasks()

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    progress['value'] = 100
    estimated_time_label.config(text="Training completed!")
    root.update_idletasks()
    logging.info("Training completed")


def create_gui():
    root = tk.Tk()
    root.title("Face Recognition Training")

    # Create a frame for the progress bar and estimated time
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a progress bar
    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress.grid(row=0, column=0, pady=10)

    # Add a label for estimated time
    estimated_time_label = ttk.Label(frame, text="Estimated time left: calculating...")
    estimated_time_label.grid(row=1, column=0, pady=5)

    def start_training():
        threading.Thread(target=train, args=(progress, estimated_time_label, root)).start()

    start_training()

    # Run the GUI event loop
    root.mainloop()


