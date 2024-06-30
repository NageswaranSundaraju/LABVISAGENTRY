from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import threading
import dlib
from imutils import face_utils  # Import face_utils for shape_to_np
from scipy.spatial import distance
import queue

# Initialize variables
current_name = "unknown"
encodings_file = "encodings.pickle"
data = pickle.loads(open(encodings_file, "rb").read())
vs = VideoStream(src=0, resolution=(640, 480)).start()  # Adjust resolution if needed
time.sleep(2.0)
fps = FPS().start()

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define indices for left and right eye landmarks
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Pre-initialize variables for optimization
gray = None
rects = []
boxes = []
encodings = []

# Define a function to calculate the eye aspect ratio
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Set thresholds and consecutive frame counters for eye blinking
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0

frame_queue = queue.Queue(maxsize=1)

# Function to put frame into the queue
def put_frame(frame):
    try:
        frame_queue.put(frame, block=False)
    except queue.Full:
        pass  # Handle queue full condition if needed

# Main thread function to display frames
def display_frames():
    while True:
        try:
            frame = frame_queue.get(block=True, timeout=0.1)
            cv2.imshow("Facial Recognition is Running", frame)
        except queue.Empty:
            pass  # Handle queue empty condition if needed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

def process_frame(frame):
    global current_name, COUNTER, gray, rects, boxes, encodings

    frame = imutils.resize(frame, width=500)  # Resize early for efficiency
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)

    names = []

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)  # Convert to NumPy array

        leftEye = shape[lStart:lEnd]  # Extract left eye landmarks
        rightEye = shape[rStart:rEnd]  # Extract right eye landmarks
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                current_name = "Liveness detected"
            COUNTER = 0

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched_idxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                if current_name != name:
                    current_name = name
                    print(current_name)
            names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

    put_frame(frame)

def process_video_stream():
    while True:
        frame = vs.read()
        process_frame(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        fps.update()

# Start processing video stream in a separate thread
thread = threading.Thread(target=process_video_stream)
thread.daemon = True
thread.start()

# Main thread continues to monitor FPS and clean up
while True:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
