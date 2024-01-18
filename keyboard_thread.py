from threading import Thread, Lock

import pyautogui

from thread_base import ThreadBase
from time import sleep
import keyboard


class KeysToPress(ThreadBase):
    def is_stopped(self):
        return self.stopped

    def __init__(self, settings, key: tuple, delay_after_stop=0, buff_to_watch=None, buffs_list=None):
        """
        Initializes the object with the given settings, key, delay_after_stop, buff_to_watch, and buffs_list.

        Parameters:
            settings (Settings): The settings to initialize the object with.
            key (tuple): The key to initialize the object with.
            delay_after_stop (int, optional): The delay after stopping the object. Defaults to 0.
            buff_to_watch (type, optional): The buff to watch. Defaults to None.
            buffs_list (type, optional): The list of buffs. Defaults to None.
        """
        self.buff_to_watch = buff_to_watch
        self.buffs_list = buffs_list
        self.settings = settings
        self.lock = Lock()
        self.stopped = True
        self.delay_after_stop = delay_after_stop
        self.key = key
        self.stopped = True

    def start(self):
        """
        Start the function.

        This function starts the thread that executes the `run` method in a separate
        thread. It sets the `stopped` attribute to `False` to indicate that the thread
        is running.

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
        Runs the function indefinitely until stopped.

        Parameters:
            None

        Returns:
            None
        """
        delay = self.delay_after_stop
        while not self.stopped:
            if len(self.key) == 1:
                self.single_button(delay)
            else:
                self.multi_buttons()

            if self.delay_after_stop != 0:
                for _ in range(int(delay / 0.5)):
                    sleep(0.5)
                    if self.stopped:
                        break
            self.stopped = True

    def multi_buttons(self):
        """
        Presses multiple buttons using the pyautogui library.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None: This function does not return anything.
        """
        for i in range(len(self.key)):
            pyautogui.press(self.key[i])

    def single_button(self,delay):
        """
        Presses a single button and performs additional actions based on the current state.

        Args:
            delay (float): The amount of delay in seconds before performing the button press.

        Returns:
            None
        """
        pyautogui.press(self.key[0])
        sleep(0.5)
        self.delay_after_stop -= 0.5
        if self.buffs_list is not None:
            how_many = 0
            while self.buff_to_watch not in self.buffs_list():
                if not self.stopped:
                    pyautogui.press(self.key[0])
                    sleep(0.5)
                    self.delay_after_stop -= 0.5

                    how_many -= 1
                    if how_many >= self.settings.HOW_MANY_BUTTON_PRESSINGS<= 0:
                        delay -= (0.7 * how_many)

    def stop(self):
        """
        Stop the function execution.

        This method sets the `stopped` attribute of the class instance to True,
        indicating that the function has stopped its execution.

        Parameters:
            None

        Returns:
            None
        """
        self.stopped = True

    def update(self, screenshot):
        """
        Updates the object with a new screenshot.

        Args:
            screenshot: The new screenshot to update the object with.

        Returns:
            None
        """
        raise NotImplementedError("update() method not implemented")
