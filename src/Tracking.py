import cv2


class Tracking:
    """
    Class which tracks an object once it has been detected. Uses the
    """

    def __init__(self):
        """
        Setup tracker class
        """
        self.tracker = cv2.TrackerKCF_create()
        self.init = False

    def track(self, frame):
        """
        Get the new bounding box
        :param frame: Next frame in video stream.
        :return: success       (bool: True if found, False if not),
                 bounding_box  (Updated bounding box [x, y, width, height])
        """
        # Check that class has been initialised
        if not self.init:
            raise Exception("Tracking class has not be initialised.")

        status, bounding_box = self.kcf_tracking.update(frame)

        # add box to image
        if status:
            p1 = (int(bounding_box[0]), int(bounding_box[1]))
            p2 = (int(bounding_box[0] + bounding_box[2]),
                  int(bounding_box[1] + bounding_box[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        return status, bounding_box

    def set_bounding_box(self, new_frame, new_box):
        """
        Used to update tracking after object detection has been run again.
        :param new_frame: Frame with object to track
        :param new_box: New bounding box around object
        """
        self.init = True
        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(new_frame, new_box)

        # Add the bounding box to the image
        p1 = (int(new_box[0]), int(new_box[1]))
        p2 = (int(new_box[0] + new_box[2]), int(new_box[1] + new_box[3]))
        cv2.rectangle(new_frame, p1, p2, (255, 0, 0), 2, 1)
