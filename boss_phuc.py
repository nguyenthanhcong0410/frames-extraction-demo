import cv2
import os
import multiprocessing
from datetime import datetime, timedelta

cv2.setNumThreads(0)

video_path = "lemon.mp4"
folder = "16-03-2026"
start_time = datetime.strptime("16-30-27", "%H-%M-%S")

if not os.path.exists(folder):
    os.makedirs(folder)


def extract_frames(start_frame, end_frame, fps):

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_count = start_frame
    save_count = start_frame // int(fps) + 1

    while frame_count < end_frame:

        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % int(fps) == 0:

            current_time = start_time + timedelta(seconds=save_count-1)
            timestamp = current_time.strftime("%H-%M-%S")

            filename = os.path.join(folder, f"frame-{save_count}_{timestamp}.jpg")

            cv2.imwrite(filename, frame)

            save_count += 1

        frame_count += 1

    cap.release()


if __name__ == "__main__":

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    cap.release()

    cpu_count = multiprocessing.cpu_count()
    frames_per_process = total_frames // cpu_count

    processes = []

    for i in range(cpu_count):

        start = i * frames_per_process
        end = total_frames if i == cpu_count - 1 else (i + 1) * frames_per_process

        p = multiprocessing.Process(target=extract_frames, args=(start, end, fps))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Done extracting frames")