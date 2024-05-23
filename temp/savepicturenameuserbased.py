import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2


# Function to capture image and save with the name from the Entry widget
def capture_image():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Get the name from the Entry widget
        image_name = entry.get()
        if image_name:
            # Save the image
            cv2.imwrite(f"{image_name}.jpg", frame)
            status_label.config(text=f"Image saved as {image_name}.jpg")
        else:
            status_label.config(text="Please enter a name for the image.")
    else:
        status_label.config(text="Failed to capture image.")


# Create the main window
root = tk.Tk()
root.title("Image Capture")

# Create and place the Entry widget
entry_label = tk.Label(root, text="Enter image name:")
entry_label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

# Create and place the capture button
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(pady=20)

# Create a status label to show messages
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
