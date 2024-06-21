from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import threading

# Initialize variables
current_name = "unknown"
encodings_file = "encodings.pickle"
data = pickle.loads(open(encodings_file, "rb").read())
vs = VideoStream(src=0, framerate=30).start()
time.sleep(2.0)
fps = FPS().start()

def process_frame(frame):
    global current_name
    frame = imutils.resize(frame, width=500)
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

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

    cv2.imshow("Facial Recognition is Running", frame)

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
