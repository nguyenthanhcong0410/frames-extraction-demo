import cv2
import os
import multiprocessing
from datetime import datetime, timedelta

cv2.setNumThreads(0)

video_folder = r"c:\Users\THANH CONG\Documents\RESFES\demo\raw video"
# Đường vào folder
script_dir = os.path.dirname(os.path.abspath(__file__))

start_times = {
    "12-03-2026": "10-00-27", # 3 dòng này có thể thay đổi tùy vào video hưng với tri quay là ngày với giờ nào
    "13-03-2026": "13-30-20",
    "16-03-2026": "20-00-30"
}

def extract_frames(video_path, output_folder, start_frame, end_frame, fps, start_time):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Cannot open video:", video_path)
        return

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_count = start_frame
    save_count = start_frame // int(fps) + 1
    interval = max(1, int(fps))

    while frame_count < end_frame:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % interval == 0:

            current_time = start_time + timedelta(seconds = save_count-1)
            timestamp = current_time.strftime("%H-%M-%S")

            filename = os.path.join(output_folder, f"frame-{save_count}_{timestamp}.jpg")

            cv2.imwrite(filename, frame)

            save_count += 1

        frame_count += 1

    cap.release()


if __name__ == "__main__":

    for video_file in os.listdir(video_folder):

        if not video_file.lower().endswith((".mp4")):
            continue

        video_path = os.path.join(video_folder, video_file)

        # Lấy ngày tháng năm từ tên video để tạo tên folder
        date_part = video_file.split("_")[-1].replace(".mp4", "")
        
        # Tạo folder trong folder "demo"
        folder = os.path.join(script_dir, date_part)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Thời gian đặt tên folder và frame dựa trên ngày trong tên video mà hưng với tri quay
        start_time_str = start_times.get(date_part)

        if start_time_str is None:
            print("No start time for date:", date_part)
            continue

        start_time = datetime.strptime(start_time_str, "%H-%M-%S")

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

            p = multiprocessing.Process(
                target = extract_frames,
                args = (video_path, folder, start, end, fps, start_time)
            )

            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    print("Done extracting frames")