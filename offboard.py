import threading
import queue
import cv2
from ultralytics import YOLO
import requests

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Video stream URL
video_url = 'http://192.0.0.4:8080/video' # Replace with your Camera's IP address

# ESP32 HTTP endpoint
ESP32_IP = "http://192.168.69.216"  # Replace with your ESP32's IP address

# Initialize the video capture
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print(f"Failed to connect to video stream at {video_url}")
    exit()

frame_queue = queue.Queue(maxsize=10)
output_queue = queue.Queue(maxsize=10)

# Variable to track the last message sent
last_message = None

# Thread to read frames from the video stream
def read_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if not frame_queue.full():
            frame_queue.put(frame)

# Thread to perform inference on frames
def process_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            results = model(frame)
            if not output_queue.full():
                output_queue.put((frame, results))

# Function to send data to the ESP32
def send_to_esp32(message):
    global last_message
    if message != last_message:  # Only send if the message has changed
        try:
            response = requests.post(f"{ESP32_IP}/data", data={"body": message})
            if response.status_code == 200:
                print(f"Message '{message}' sent successfully.")
                last_message = message
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

# Start the threads
read_thread = threading.Thread(target=read_frames, daemon=True)
process_thread = threading.Thread(target=process_frames, daemon=True)
read_thread.start()
process_thread.start()

# Display the processed frames and send messages based on detection
while True:
    if not output_queue.empty():
        frame, results = output_queue.get()

        # Check if any person is detected
        person_detected = False
        for result in results:
            for detection in result.boxes.data.tolist():
                class_id = int(detection[5])
                if class_id == 0:  # Class ID 0 is 'person'
                    person_detected = True
                    x1, y1, x2, y2 = map(int, detection[:4])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, 'Person', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Send "l" if a person is detected, otherwise "r"
        if person_detected:
            send_to_esp32("l")
        else:
            send_to_esp32("r")

        # Display the frame
        cv2.imshow('YOLOv8 Person Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
