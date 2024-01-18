from copy import copy
from threading import Thread, Lock
from time import time

import cv2 as cv

from Helpers.entity import Entity
from screenshot import Screenshot
from thread_base import ThreadBase


class Detection(ThreadBase):

    def is_stopped(self):
        """
        Return if the object is stopped.

        Returns:
            bool: True if the object is stopped, False otherwise.
        """
        return self.stopped

    def __init__(self, settings, patterns: list[Entity], ss_method: Screenshot.get_screenshot):
        self.settings = settings
        self.lock = Lock()
        self.stopped = True
        self.fps = 0
        self.gfx_pattern = None
        self.name = None
        self.result = None
        self.threshold = None

        self.detection_result = None
        self.entities = []
        self.entities = patterns
        self.lock = Lock()
        self.ss_method = ss_method

    def start(self):
        """
        Runs the main loop of the program.

        This function continuously scans for save zones and buffs in the given image.
        It uses the self.ss_method() to capture the image. If no image is captured, the function continues to the next iteration of the loop.

        For each entity in self.entities, the function extracts the region of interest (ROI) from the captured image based on the entity's corner and offset.
        It then performs template matching using the entity's pattern and the ROI. If the maximum correlation value exceeds the threshold, the entity's name is added to the detection_result list.

        After scanning for save zones, the function proceeds to scan for buffs using the patterns defined in self.settings.BUFFS_PATTERNS.
        The same template matching process is applied to each buff pattern, and if a match is found, the buff's name is added to the detection_result list.

        The elapsed time for each iteration of the loop is measured using the time() function, and the resulting value is stored in self.fps.
        The detection_result list is copied and stored in self.detection_result.

        Note: Some commented code for visualizing the detected regions and images is provided but currently disabled.

        Args:
            None

        Returns:
            None
        """
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def run(self):
        """
        Runs the main loop of the program.

        This function continuously scans for save zones and buffs in the provided image.
        It uses various image processing techniques to detect the entities and determine
        their positions within the image.

        Parameters:
            None

        Returns:
            None
        """
        while not self.stopped:
            start_time = time()

            # ------------------------ SCAN FOR SAVE ZONE --------------------------
            image = self.ss_method()
            if image is None:
                continue
            detection_result = []
            for i in range(len(self.entities)):
                x, y = self.entities[i].corner
                w, h = self.entities[i].offset

                roi = image[y:y + h, x:x + w]

                gfx_pattern = self.entities[i].pattern
                name = self.entities[i].name
                result = cv.matchTemplate(roi, gfx_pattern, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                threshold = 0.70

                if max_val >= threshold:
                    detection_result.append(name)

            # ------------------------ SCAN FOR BUFFS --------------------------

            buffs = self.settings.BUFFS_PATTERNS
            for i in range(len(buffs)):
                x, y = buffs[i].corner
                w, h = buffs[i].offset

                roi = image[y:y + h, x:x + w]

                gfx_pattern = buffs[i].pattern
                name = buffs[i].name
                result = cv.matchTemplate(roi, gfx_pattern, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

                threshold = 0.80
                if max_val >= threshold:
                    detection_result.append(name)
                    # w, h, channels = gfx_pattern.shape
                    # cv.rectangle(roi, max_loc, (max_loc[0] + h, max_loc[1] + w), 255, 2)
                    # cv.imshow("roi", roi)
                    # cv.waitKey(1)

            elapsed_time = time() - start_time
            self.lock.acquire()
            self.fps = elapsed_time
            self.detection_result = copy(detection_result)
            self.lock.release()

    def stop(self):
        self.stopped = True

    def get_matches(self):
        """
        Retrieve the current value of the detection result.

        Returns:
            The current value of the detection result.
        """
        self.lock.acquire()
        result = self.detection_result
        self.lock.release()
        return result

    def get_fps(self):
        """
        Calculate and return the frames per second (FPS) of the detection.

        Returns:
            str: The FPS of the detection formatted to 2 decimal places.
        """
        fps = 0
        if self.fps > 0:
            fps = 1 / self.fps
        return f"Detection :{fps:.2f}"

    def update(self, screenshot):
        pass
