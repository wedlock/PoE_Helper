import re

from enum import Enum
from time import sleep

import cv2 as cv
import numpy as np
import psutil
import pyautogui
import tesserocr
from loguru import logger
from pywinauto import Application, ElementNotFoundError

from Helpers.entity import Entity
from windowcapture import WindowCapture
from PIL import Image


class State(Enum):
    NO_GAME = 0
    GAME_SYNC_SCREEN = 1
    LOGIN_SCREEN = 2
    SELECT_CHAR_SCREEN = 3
    GAME_IS_READY = 4
    UNKNOWN = 5


class ExecuteGame:
    def __init__(self, settings):
        """
        Initializes class with have to job find game process and run game / login and create proper game instance.
        Entry point is a method run()
        Args:
            settings (Settings): A dictionary containing the settings used in bot.

        Returns:
            None
        """
        self.settings = settings
        self.chars = {}

    @staticmethod
    def is_process_running(process_name):
        """
        Check if a process with the given name is currently running.

        Args:
            process_name (str): The name of the process to check.

        Returns:
            bool: True if the process is running, False otherwise.
        """
        # dupa=psutil.process_iter()
        procesy = [p.name() for p in psutil.process_iter()]
        if process_name in procesy:
            return True

        return False

    def find_game_window(self):
        pass

    def find_entity_in_container(self, name: str):
        """
        Find an entity in the container by its name.

        Parameters:
            name (str): The name of the entity to search for.

        Returns:
            entity: The entity with the specified name, or None if it is not found.
        """
        entity = None
        for i in range(len(self.settings.GAME_WINDOW_PATTERNS)):
            if self.settings.GAME_WINDOW_PATTERNS[i].name == name:
                entity = self.settings.GAME_WINDOW_PATTERNS[i]
                break
        return entity

    def run_game(self):
        """
        Runs the game by performing a series of actions.

        This function is responsible for running the game by performing a series of actions. It starts by pressing the 'winleft' key and then pressing 'd' to minimize all windows. After waiting for 1 second, it captures a screenshot of the game window using the WindowCapture class. It then searches for the entity named "PoE" within the screenshot using the find_entity_in_container method. The function then applies template matching using the cv.matchTemplate function to find the best match for the entity pattern within the screenshot. If the maximum correlation coefficient is greater than or equal to 0.8, it means a match is found. In that case, it determines the coordinates of the top-left corner of the matched entity and moves the mouse cursor to the center of the entity using pyautogui.moveTo. It then performs a double click using pyautogui.doubleClick. Finally, it presses the 'winleft' key and then presses 'd' again to restore the minimized windows.

        Parameters:
            None

        Returns:
            None
        """

        pyautogui.keyDown('winleft')
        pyautogui.press('d')
        pyautogui.keyUp('winleft')
        sleep(1)
        wincap = WindowCapture()

        ss = wincap.get_screenshot()
        entity = self.find_entity_in_container("PoE")

        result = cv.matchTemplate(ss, entity.pattern, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val >= 0.8:
            top_left = max_loc
            h, w, a = entity.pattern.shape

            pyautogui.moveTo(top_left[0] + w // 2, top_left[1] + h // 2)
            pyautogui.doubleClick()
            pyautogui.keyDown('winleft')
            pyautogui.press('d')
            pyautogui.keyUp('winleft')

    def set_focus(self, window_name: str):
        """
        Sets the focus to a window with the given name.

        Parameters:
            window_name (str): The name of the window to set focus to.

        Returns:
            bool: True if the focus was successfully set, False otherwise.
        """
        try:
            app = Application().connect(title=window_name)
        except ElementNotFoundError:
            if self.settings.DEBUG_MODE:
                logger.warning(f'No window with name {window_name} found')
            return False
        w = app.window(title=window_name)
        w.set_focus()
        return True

    def find_login_screen(self):
        """
        Finds the login screen in the game window.

        Returns:
            bool: True if the login screen is found, False otherwise.
        """
        self.set_focus(self.settings.GAME_WINDOW_NAME)
        wincap = WindowCapture()
        ss = wincap.get_screenshot()
        entity = self.find_entity_in_container("LOGIN")
        result = cv.matchTemplate(ss, entity.pattern, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val >= 0.8:
            top_left = max_loc
            h, w, a = entity.pattern.shape
            # pyautogui.moveTo(top_left[0] + w // 2, top_left[1] + h // 2)
            # pyautogui.click()
            loc = (top_left[0] + w // 2, top_left[1] + h // 2)
            self.set_entity_corner(entity, loc)
            return True
        return False

    def set_entity_corner(self, entity: Entity, corner):
        """
        Set the corner of an entity in the game window patterns.

        Args:
            entity (Entity): The entity whose corner will be set.
            corner: The corner value to set.

        Returns:
            None
        """
        for i in range(len(self.settings.GAME_WINDOW_PATTERNS)):
            if self.settings.GAME_WINDOW_PATTERNS[i].name == entity.name:
                self.settings.GAME_WINDOW_PATTERNS[i].corner = corner
                break

    def login(self):
        """
        Logs into the system using a predefined login entity.

        Parameters:
            self (ClassName): An instance of the ClassName.

        Returns:
            None
        """
        entity = self.find_entity_in_container("LOGIN")
        x, y = entity.corner
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.typewrite(".......") # ENTER UR PASSWORD HERE
        pyautogui.press('enter')

    def find_select_char_screen(self):
        """
        Find and select the character screen.

        Returns:
            bool: True if the character screen is found and selected, False otherwise.
        """
        self.set_focus(self.settings.GAME_WINDOW_NAME)
        wincap = WindowCapture()
        ss = wincap.get_screenshot()
        entity = self.find_entity_in_container("CHAR_SELECT_SCRN")
        result = cv.matchTemplate(ss, entity.pattern, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val >= 0.8:
            top_left = max_loc
            h, w, a = entity.pattern.shape
            # pyautogui.moveTo(top_left[0] + w // 2, top_left[1] + h // 2)
            # pyautogui.click()
            loc = (top_left[0] + w // 2, top_left[1] + h // 2)
            self.set_entity_corner(entity, loc)
            return True
        return False

    def find_chars(self):
        """
        Finds and returns the coordinates of characters in the game window.

        This method is responsible for locating characters in the game window and returning their coordinates. It uses computer vision techniques to match a template of a character with the screenshot of the game window. The method then extracts the coordinates of the matched characters and stores them in a dictionary.

        Returns:
            chars (dict): A dictionary containing the names of the characters as keys and their corresponding coordinates as values.

        """
        chars = {}
        self.set_focus(self.settings.GAME_WINDOW_NAME)
        wincap = WindowCapture()
        ss = wincap.get_screenshot()
        entity = self.find_entity_in_container("CHAR_CORNERS")
        result = cv.matchTemplate(ss, entity.pattern, cv.TM_CCOEFF_NORMED)

        loc = np.where(result >= 0.8)
        points = list(zip(*loc[::-1]))

        for point in points:
            top_left = point
            h, w, _ = entity.pattern.shape
            bottom_right = (top_left[0] + 300, top_left[1] + h)
            top_left = (top_left[0], top_left[1])
            cv.rectangle(ss, top_left, bottom_right, (0, 0, 255), 2)
            x = top_left[0]
            y = top_left[1]
            w1 = 300
            h1 = h
            crop = ss[y + 6:y + h1 + 6, x + 10:x + w1]

            crop2 = Image.fromarray(crop)
            char_name = tesserocr.image_to_text(crop2)
            clean_text = re.sub(r'[^\w\s]', '', char_name)
            # clean_text = clean_text[:-2]

            centered_point = [point[0] + w1 // 2, point[1] + h1 // 2]
            chars[clean_text[:-1].lower()] = centered_point

        if self.settings.DEBUG_MODE:
            logger.info(f'Found char: {chars.keys()}')
        return chars

    def select_char(self, character_name):
        """
        Selects a character by name and performs a double click action on the character's location.

        Args:
            character_name (str): The name of the character to select.

        Returns:
            None
        """
        if character_name in self.chars:
            x, y = self.chars[character_name]
            pyautogui.moveTo(x, y)
            pyautogui.doubleClick()

    def find_game_is_ready(self):
        """
        Finds out if the game is ready by performing a series of steps:

        1. Sets the focus to the game window.
        2. Captures a screenshot of the game window.
        3. Searches for the entity with the name "GAME_INSTANCE" in the captured screenshot.
        4. Matches the template of the entity with the captured screenshot using OpenCV's matchTemplate function.
        5. Finds the maximum value and location of the match result.
        6. Checks if the maximum value is greater than or equal to 0.8.
        7. Returns True if the game is ready, False otherwise.

        Returns:
            bool: True if the game is ready, False otherwise.
        """
        self.set_focus(self.settings.GAME_WINDOW_NAME)
        wincap = WindowCapture()
        ss = wincap.get_screenshot()
        entity = self.find_entity_in_container("GAME_INSTANCE")
        result = cv.matchTemplate(ss, entity.pattern, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val >= 0.8:
            return True
        return False

    # * ----------------------------- main logic section ----------------------------

    def where_we_are(self):
        """
        Checks the current state of the program and returns the corresponding state value.

        Returns:
            State: The state of the program. Possible values are:
                - State.NO_GAME: If the game process is not running.
                - State.LOGIN_SCREEN: If the login screen is found.
                - State.SELECT_CHAR_SCREEN: If the select character screen is found.
                - State.GAME_IS_READY: If the game is ready to be played.
                - State.UNKNOWN: If the state of the program is unknown.
        """
        if not self.is_process_running(self.settings.GAME_PROCESS_NAME):
            return State.NO_GAME
        if self.find_game_window():
            return State.NO_GAME
        # if self.find_sync_screen():
        #     return State.GAME_SYNC_SCREEN

        if self.find_login_screen():
            return State.LOGIN_SCREEN
        if self.find_select_char_screen():
            return State.SELECT_CHAR_SCREEN
        if self.find_game_is_ready():
            return State.GAME_IS_READY

        return State.UNKNOWN

    def run(self):
        """
        Runs the main loop of the program.

        This function continuously checks the current state of the game and performs
        the necessary actions based on the state. It handles scenarios such as launching
        the game, logging in, selecting a character, and handling unknown screens.

        Returns:
            None
        """
        we_are_done = True

        while we_are_done:

            import keyboard

            if (keyboard.is_pressed(self.settings.EXIT_SHORTCUT[0])
                    and keyboard.is_pressed(self.settings.EXIT_SHORTCUT[1])):
                if self.settings.DEBUG_MODE:
                    logger.info(f'Exit shortcut pressed, exiting from botting')
                quit(0)
            we_are_here = self.where_we_are()

            if we_are_here == State.NO_GAME:
                if self.settings.DEBUG_MODE:
                    logger.info(f'Launch game.exe')
                self.run_game()

            if we_are_here == State.LOGIN_SCREEN:
                if self.settings.DEBUG_MODE:
                    logger.info(f'Found login screen, try to login')
                self.chars = {}
                self.login()

            if we_are_here == State.SELECT_CHAR_SCREEN:
                if self.settings.DEBUG_MODE:
                    logger.info(f'Found select char screen')
                if len(self.chars) == 0:
                    self.chars = self.find_chars()
                if self.settings.DEBUG_MODE:
                    logger.info(f'Chars: {self.chars}')
                self.select_char(self.settings.CHARACTER_NAME)
                if self.settings.DEBUG_MODE:
                    logger.info(f'Char selected: {self.settings.CHARACTER_NAME}')

            if we_are_here == State.UNKNOWN:
                if self.settings.DEBUG_MODE:
                    logger.info(f'Unknown screen')
                self.chars = {}

            if we_are_here == State.GAME_IS_READY:
                if self.settings.DEBUG_MODE:
                    logger.success(f'Game is ready for botting')
                we_are_done = False
