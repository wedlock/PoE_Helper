import cv2 as cv
import os
from Helpers.CreateData import CreateData


class Settings:
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    DEBUG_MODE = True
    CV_IMAGE_FORMAT = cv.COLOR_RGB2BGR

    TO_FIND_IN_SCREEN = None
    GAME_WINDOW_PATTERNS = None
    BUFFS_PATTERNS = None
    GAME_WINDOW_NAME = 'Path of Exile'
    GAME_PROCESS_NAME = 'PathOfExile.exe'
    CHARACTER_NAME = 'ENTER HERE CHARNAME'
    HOW_MANY_BUTTON_PRESSINGS = 5
    SAFE_ZONES = None
    EXIT_SHORTCUT = ['ctrl','x']



    def __init__(self):
        self.BUFF = None

    def initialize(self):
        """
        Initializes the object by setting up the necessary variables and data structures.

        Parameters:
            self (object): The object itself.

        Returns:
            None
        """
        self.CV_IMAGE_FORMAT = cv.COLOR_RGB2BGR
        cd = CreateData(self)
        self.TO_FIND_IN_SCREEN, self.GAME_WINDOW_PATTERNS, self.BUFFS_PATTERNS = cd.create_all_data()
        self.SAFE_ZONES = cd.create_safe_zones_names()
