import re
from copy import copy
from threading import Thread, Lock
from time import time

import cv2 as cv
import tesserocr
from PIL import Image

from screenshot import Screenshot
from thread_base import ThreadBase


def get_xy_wh(corners, offsets):
    x = corners[0]
    y = corners[1]
    w = offsets[0]
    h = offsets[1]
    return x, y, w, h


class Health(ThreadBase):
    def is_stopped(self):
        return self.stopped

    OCR_OPTIONS = r'--psm 7 --oem 3 digit=1234567890'
    LIFE_CORNER = [96 - 7, 831]
    LIFE_OFFSET = [41 + 6, 22]
    MAXLIFE_CORNER = [138, 831]
    MAXLIFE_OFFSET = [41, 22]

    def __init__(self, settings, ss_method: Screenshot.get_screenshot):

        """
        Class running in thread and read on screen 2 elements:
        Player health and max health

        Args:
            settings (Any): The settings object.
            ss_method (function): The get_screenshot method.

        Returns:
            None
        """
        self.screenshot = None
        self.settings = settings
        self.lock = Lock()
        self.stopped = True
        self.fps = 0

        self.current_hp = 0
        self.max_hp = 0
        self.get_screenshot = ss_method

    def start(self):
        """
        Starts the thread that runs the 'run' method.

        This method sets the 'stopped' attribute to False and creates a new thread with the 'run' method as the target. The thread is then started.

        Parameters:
            None

        Returns:
            None
        """
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def run(self):
        """
        Runs the function in a loop until `self.stopped` is set to True.
        Captures a screenshot and performs image processing operations to extract health information.

        Parameters:
            None

        Returns:
            None
        """
        while not self.stopped:
            start_time = time()
            image = self.get_screenshot()

            if image is None:
                continue
            gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            # CURRENT HEALTH
            x, y, w, h = get_xy_wh(self.LIFE_CORNER, self.LIFE_OFFSET)
            crop = gray_image[y:y + h, x:x + w]


            _, black_image = cv.threshold(crop, 185, 255, cv.THRESH_BINARY)
            cv.imshow('black', black_image)
            cv.moveWindow('black', 1920, 700)
            cv.waitKey(1)

            crop2 = Image.fromarray(black_image)
            health_current = tesserocr.image_to_text(crop2)


            # MAX HEALTH
            x, y, w, h = get_xy_wh(self.MAXLIFE_CORNER, self.MAXLIFE_OFFSET)
            crop = gray_image[y:y + h, x:x + w]
            _, black_image = cv.threshold(crop, 185, 255, cv.THRESH_BINARY)
            crop2 = Image.fromarray(black_image)

            health_max = tesserocr.image_to_text(crop2)
            max_hp = re.sub(r'\D', "", health_max)
            current_hp = re.sub(r'\D', "", health_current)

            elapsed_time = time() - start_time

            self.lock.acquire()
            self.current_hp = copy(current_hp)
            self.max_hp = copy(max_hp)
            self.fps = elapsed_time
            self.lock.release()

    def stop(self):
        self.stopped = True

    def get_hp(self):
        """
        Return the current and maximum hit points of the object.

        :returns: A tuple containing the current hit points and the maximum hit points.
        :rtype: tuple
        """
        result = (self.current_hp, self.max_hp)
        return result

    def get_fps(self):
        """
        Calculates the frames per second (FPS) based on the current value of self.fps.

        Returns:
            str: A formatted string representing the FPS value as "Health: {fps:.2f}".
        """
        fps = 0
        if self.fps > 0:
            fps = 1 / self.fps
        return f"Health: {fps:.2f}"

    def update(self, screenshot):
        """
        Update the screenshot with the given image.

        :param screenshot: The new screenshot image.
        :type screenshot: Image

        :return: None
        """
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
