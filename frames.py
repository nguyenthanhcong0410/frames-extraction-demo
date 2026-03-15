import cv2
import os

raw_video = "green_apple.mp4"
folder = "frames"

#create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(raw_video)

frame_in_second = cap.get(cv2.CAP_PROP_FPS)
interval = int(frame_in_second) #tui để đại ở đây là mỗi frame cách nhau 1s nha, mốt có data của hưng rồi thì đổi sau cũng được

save_count = 0
frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if frame_count % interval == 0:
        save_frame_name = os.path.join(folder, f"frame_{save_count}.jpg")
        cv2.imwrite(save_frame_name, frame)
        save_count += 1
    
    frame_count += 1
    

cap.release()

print(f"Done {save_count} frames")