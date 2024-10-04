import cv2
import os
from datetime import datetime

class SnapshotManager:
    def __init__(self):
        self.video_writer = None
        self.recording = False

    def save_snapshot(self, frame):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = f"./assets/saved_frames/frame_{timestamp}.png"
        cv2.imwrite(path, frame)

    def start_video_recording(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.video_writer = cv2.VideoWriter(f"./assets/videos/video_{timestamp}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))
        self.recording = True

    def stop_video_recording(self):
        if self.video_writer:
            self.video_writer.release()
        self.recording = False
