from Tracking import Tracking
from VideoCapture import VideoCapture
import cv2
import datetime
from YoloDetector import YoloDetector


def main(disp_stream=False, n_detection_frames=100):

    # Init important classes
    vid_cap = VideoCapture()
    tracker = Tracking()
    yolo = YoloDetector()

    detection_count = 0
    tracking_status = False
    detection_status = False
    recording = False

    # Main camera loop
    vid_cap.start()
    while True:
        # Run detection algorythm every n_detection_frames frames or if
        # tracking has failed but still detected
        if detection_count == n_detection_frames:
            # run detection
            detection_status, bounding_box = yolo.detect(
                vid_cap.video_buffer[-1])

            # If we see something then init the tracking and recording
            if detection_status:
                tracker.set_bounding_box(vid_cap.video_buffer[-1], bounding_box)

                # If we arnt recording yet then start
                if not recording:
                    print("Recording stated.")
                    now = datetime.datetime.now()
                    file_name = "./Videos/" + str(now.date()) + "_" + str(
                        now.time()) + ".avi"
                    vid_cap.start_record(file_name)
                    recording = True

            # If we didn't see anything, but we are recording then stop
            elif not detection_status and recording:
                print("Recording ended.")
                vid_cap.end_record()
                recording = False

            detection_count = 0
        else:
            detection_count += 1

        # If object has been detected, run the tracking algorythm
        if detection_status:
            tracking_status, bounding_box = tracker.track(
                vid_cap.video_buffer[-1])

            # If tracking is good then no need for detection
            if tracking_status:
                detection_count = 0

        # Display the frame
        if disp_stream:
            vid_cap.display_frame()

        # End the stream
        key = cv2.waitKey(1)
        if vid_cap.status is False or key == ord('q'):
            break
    vid_cap.close()


if __name__ == "__main__":
    main(True)
