import cv2
import os

def save_frame_with_boxes(frame, result):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = f"./assets/saved_frames/frame_{timestamp}.png"
    if not os.path.exists('./assets/saved_frames'):
        os.makedirs('./assets/saved_frames')
    cv2.imwrite(path, frame)
