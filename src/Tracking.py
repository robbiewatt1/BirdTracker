import cv2


class Tracking:
    """
    Class which tracks an object once it has been detected. Uses the
    """

    def __init__(self, init_frame, init_box):
        """
        :param init_frame: First frame where object has been detected.
        :param init_box: Initial bounding box of object [x, y, width, height].
        """
        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(init_frame, init_box)

    def track(self, frame):
        """
        Get the new bounding box
        :param frame: Next frame in video stream.
        :return: success       (bool: True if found, False if not),
                 bounding_box  (Updated bounding box [x, y, width, height])
        """
        return self.kcf_tracking.update(frame)

    def set_bounding_box(self, new_frame, new_box):
        """
        Used to update tracking after object detection has been run again.
        :param new_frame: Frame with object to track
        :param new_box: New bounding box around object
        """
        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(new_frame, new_box)
