import os
import cv2
import tkinter as tk
from tkinter import simpledialog, messagebox


# Function to capture images
def capture_images(username):
    # Define the parent directory
    parent_dir = "dataset"

    # Create the parent directory if it doesn't exist
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    # Create a directory for the user inside the parent directory
    user_dir = os.path.join(parent_dir, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        messagebox.showerror("Error", "Could not open camera.")
        return

    # Capture 10 images
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            messagebox.showerror("Error", "Could not read frame.")
            break
        # Save the frame as an image file
        img_path = os.path.join(user_dir, f"image_{i + 1}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Captured {img_path}")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Info", "Images captured successfully.")






