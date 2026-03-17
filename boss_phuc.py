import cv2
import os
from datetime import datetime, timedelta

raw_video_12h = "lemon.mp4"
folder = "16-03-2026"

#create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(raw_video_12h)
if not cap.isOpened():
    print(f"Cannot open video {raw_video_12h}")
    exit()

frame_in_second = cap.get(cv2.CAP_PROP_FPS)
print(f"Frames per second: {frame_in_second}")
interval = int(frame_in_second) #tui để ở đây mỗi frame cách nhau 1s nha, mốt có data của hưng ròi thì đổi lại cũng được

save_count = 1
frame_count = 0
start_time = datetime.strptime("16-30-27", "%H-%M-%S")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if frame_count % interval == 0:
        current_time = start_time + timedelta(seconds = save_count - 1)
        timestamp = current_time.strftime("%H-%M-%S")
        
        save_frame_name = os.path.join(folder, f"frame-{save_count}_{timestamp}.jpg")
        print(os.path.abspath(save_frame_name))
        
        test_saved = cv2.imwrite(save_frame_name, frame)
        print("Saved:", test_saved)
        save_count += 1
    
    frame_count += 1

cap.release()

print(f"Done {save_count - 1} frames")