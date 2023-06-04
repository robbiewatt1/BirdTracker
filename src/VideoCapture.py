import time
import cv2
from threading import Thread
from collections import deque
from queue import Queue


import random
def test_record():
    return random.random() < 0.0001


class VideoCapture:

    # Mian class for capturing images from the camera and saving .
    def __init__(self, cam_id=0, buff_length=300):
        """
        :param cam_id: ID of the camera being used (will probably be 0 if
          only 1 camera is connected).
        :param buff_length: Number of frames in the buffer. For 30fps camera,
         this defaults to 10s.
        """

        # Open camera stream
        self.vid_cap = cv2.VideoCapture(cam_id)
        if self.vid_cap.isOpened is False:
            raise ConnectionError(f"Cannot open camera with id {cam_id}.")
        self.fps = self.vid_cap.get(cv2.CAP_PROP_FPS)

        # Read first frame to get buffer size
        (self.status, image) = self.vid_cap.read()
        self.frame_shape = image.shape

        # Set the buffer to make sure we recorded frames before
        self.video_buffer = deque(maxlen=buff_length)
        self.video_buffer.append(image)

        # Set the capture thread and make it daemon (run in background)
        self.get_frame_thread = Thread(target=self.get_frame, args=())
        self.get_frame_thread.daemon = True

        # Set the variables used to save the video
        self.writer = None              # Will be instanced of cv2.VideoWriter
        self.write_frame_thread = None  # Thread for writing video
        self.record = False             # Checks if we are saving the video
        self.record_buffer = Queue()    # Buff containing frames to be saved

    def set_camera_property(self, property_kv_list):
        """
        Set properties of the camera (e.g. frame rate / resolution)
        :param property_kv_list: List of key / value pairs for camera settings
        """
        for param in property_kv_list:
            self.vid_cap.set(param[0], param[1])

    def start(self):
        """
        Starts the capture thread
        """
        self.get_frame_thread.start()

    def get_frame(self):
        """
        Thread function to constantly get new frames and add them to the buffer
        """
        while True:
            (self.status, frame) = self.vid_cap.read()
            if self.status is False:
                print("[Exiting] Can't read any more frames.")
                break
            else:
                self.video_buffer.append(frame)
                if self.record:
                    self.record_buffer.put(frame)

        self.vid_cap.release()

    def display_frame(self, bounding_box=None):
        """
        Function which displays most recent thread from buffer to screen
        """
        if self.status:
            cv2.imshow('frame', self.video_buffer[-1])

    def start_record(self, file_path):
        """
        Function called to start recording and saving video.
        :param file_path: Path where video is saved.
        """
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.writer = cv2.VideoWriter(file_path, fourcc, self.fps,
                                      (self.frame_shape[1], self.frame_shape[0]
                                       ), True)

        # Add the video buffer to the record
        for frame in self.video_buffer:
            self.record_buffer.put(frame)

        self.write_frame_thread = Thread(target=self.write_frame, args=())
        self.write_frame_thread.daemon = True
        self.record = True
        self.write_frame_thread.start()

    def write_frame(self):
        """
        Thread function used to write frames to disk
        """
        while True:
            # Check if recording is done
            if not self.record and self.record_buffer.empty():
                return
            # Check if anything in queue. If not then sleep till there is
            if self.record_buffer.empty():
                time.sleep(1.)
            else:
                self.writer.write(self.record_buffer.get())

    def end_record(self):
        """
        Function called to end video being saved.
        """
        self.record = False
        self.write_frame_thread.join()
        self.writer.release()


if __name__ == "__main__":

    vid_cap = VideoCapture()
    vid_cap.start()

    while True:
        vid_cap.display_frame()

        key = cv2.waitKey(1)
        if key == ord('s') and not vid_cap.record:
            print("start")
            vid_cap.start_record("./example.avi")

        key = cv2.waitKey(1)
        if vid_cap.record and key == ord('e'):
            print("End")
            vid_cap.end_record()

        key = cv2.waitKey(1)
        if vid_cap.status is False or key == ord('q'):
            break

