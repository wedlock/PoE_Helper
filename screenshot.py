from threading import Thread, Lock
from time import time, sleep
import cv2 as cv

import windowcapture as wincap
from thread_base import ThreadBase


class Screenshot(ThreadBase):
    def is_stopped(self):
        return self.stopped

    def __init__(self, settings,game_window_name: str = 'Path of Exile'):
        """
        Initializes the class instance with the given settings and game window name.

        Args:
            settings: The settings object for the class instance.
            game_window_name (str): The name of the game window. Defaults to 'Path of Exile'.
        """
        self.settings = settings
        self.fps = 0
        self.lock = Lock()
        self.stopped = True

        self.screenshot = None
        self.game_windows_name = game_window_name


    def start(self):
        """
        Starts the function execution by setting the `stopped` attribute to False and creating a new thread to run the `run` method.

        Parameters:
            None

        Returns:
            None
        """
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def update(self, screenshot):
        pass

    def run(self):
        """
        Runs the function continuously until it is stopped.

        This function captures screenshots using the `WindowCapture` class and updates the `screenshot` attribute of the object. It uses a `while` loop to continuously capture screenshots until the `stopped` attribute is set to `True`.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None

        Raises:
        - None
        """
        wc = wincap.WindowCapture(self.game_windows_name)
        while not self.stopped:
            start_time = time()
            self.lock.acquire()
            self.screenshot = wc.get_screenshot()
            sleep(0.1)

            elapsed_time = time() - start_time
            self.fps = elapsed_time
            self.lock.release()


    def get_screenshot(self):
        """
        Get the screenshot.

        Returns:
            The screenshot.
        """
        return self.screenshot

    def get_fps(self):
        """
        Calculate the frames per second (FPS) of the screenshot.

        Returns:
            str: A string representing the FPS of the screenshot, formatted to two decimal places.
        """
        fps = 0
        if self.fps > 0:
            fps = 1 / self.fps
        return f"Screenshot :{fps:.2f}"


