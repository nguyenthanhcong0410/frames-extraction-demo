import cv2
import os


raw_video = "green_apple.mp4"

folder = "frames"

#create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(raw_video)

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frame_name = os.path.join(folder, f"frame_{frame_count}.jpg")
    
    #save frame as image
    cv2.imwrite(frame_name, frame)
    frame_count += 1

cap.release()

print(f"Done extracting {frame_count} frames")