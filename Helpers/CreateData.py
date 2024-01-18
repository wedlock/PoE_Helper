import os.path
from enum import Enum

import cv2 as cv
from loguru import logger

from Helpers.entity import Entity

safe_zone_images = {"INVENTORY": "Assets/INVENTORY.png",
                    "STASH": "Assets/STASH.png",
                    "EDIT": "Assets/EDIT.png",
                    "ATLAS_SKILLS": "Assets/ATLASSKILLS.png",
                    "ATLAS": "Assets/ATLAS.png",
                    "CHARACTER": "Assets/CHARACTER.png",
                    "OPTIONS": "Assets/OPTIONS.png",
                    "SKILLS": "Assets/SKILLS.png",
                    "SOCJAL": "Assets/SOCJAL.png",
                    "SUBTERRANEAN": "Assets/SUBTERRANEAN.png",
                    }

safe_zone_offset = {"INVENTORY": [289, 93],
                    "STASH": [248, 60],
                    "EDIT": [104, 125],
                    "ATLAS_SKILLS": [251, 69],
                    "ATLAS": [251, 69],
                    "CHARACTER": [248, 60],
                    "OPTIONS": [248, 60],
                    "SKILLS": [251, 69],
                    "SOCJAL": [248, 60],
                    "SUBTERRANEAN": [830 + 258, 30]
                    }

safe_zone_corners = {"INVENTORY": [1444, 23],
                     "STASH": [205, 36],
                     "EDIT": [956, 936],
                     "ATLAS_SKILLS": [832, 33],
                     "ATLAS": [832, 33],
                     "CHARACTER": [205, 36],
                     "OPTIONS": [205, 36],
                     "SKILLS": [832, 33],
                     "SOCJAL": [205, 36],
                     "SUBTERRANEAN": [830, 42]
                     }

game_window = {"CHAR_SELECT_SCRN": "Assets/CHAR_SELECT_SCRN.png",
               "LOGIN": "Assets/LOGIN.png",
               "PoE": "Assets/PoE.png",
               "CHAR_CORNERS": "Assets/CHAR_CORNERS.png",
               "GAME_INSTANCE": "Assets/GAME_INSTANCE.png",
               }
buffs = {
    "BONE ARMOR": "Assets/BONE ARMOR.png",
    "GUARDIAN": "Assets/GUARDIAN.png",
    "SPECTRE": "Assets/SPECTRE.png",
    "HASTE": "Assets/HASTE.png",

    "VITALITY": "Assets/VITALITY.png",
    "GOLEM": "Assets/GOLEM.png",
    # "Haste": "Assets/HASTE.png"
}

buffs_offset = [1574, 80]
buffs_corner = [0, 0]


class ContainerType(Enum):
    GAME_WINDOW = 1
    SAFE_ZONE = 2
    BUFFS = 3


class CreateData:
    def __init__(self, settings):
        """
        Initialize the object with the given settings.

        Parameters:
            settings (any): The settings to be used by the object.

        Returns:
            None
        """
        self.settings = settings

    def _create_entities(self, images, corners, offsets, entity_type):
        """
        Creates a list of Entity objects based on the given images, corners, offsets, and entity_type.

        Parameters:
            images (dict): A dictionary containing the images as keys and their corresponding values.
            corners (dict): A dictionary containing the corners as keys and their corresponding values.
            offsets (dict): A dictionary containing the offsets as keys and their corresponding values.
            entity_type (enum): An enum representing the type of entity.

        Returns:
            list: A list of Entity objects created based on the given parameters.
        """
        result = []

        for key in images.keys():
            item = Entity()
            item.name = key
            item.pattern = self._try_load_image(images[key])

            if entity_type == ContainerType.SAFE_ZONE:
                item.corner = corners[key]
                item.offset = offsets[key]

            if entity_type == ContainerType.GAME_WINDOW:
                item.corner = None
                item.offset = None

            if entity_type == ContainerType.BUFFS:
                item.corner = corners
                item.offset = offsets
            result.append(item)
        return result

    def _create_game_window_entities(self, images):
        """
        Creates game window entities based on the given images.

        Parameters:
            images (dict): A dictionary mapping entity names to image paths.

        Returns:
            list: A list of created Entity objects.
        """
        result = []
        item = Entity()
        for key in images.keys():
            item.name = key
            item.pattern = self._try_load_image(images[key])
            item.corner = None
            item.offset = None
            result.append(item)
        return result

    def _try_load_image(self, path):
        """
        Tries to load an image given a file path.

        Args:
            path (str): The path to the image file.

        Returns:
            numpy.ndarray or None: The loaded image if it exists, None otherwise.
        """
        file_path = path
        file = os.path.join(self.settings.CURRENT_PATH, file_path)

        if os.path.exists(file):
            cvimage = cv.imread(file, self.settings.CV_IMAGE_FORMAT)
            if self.settings.DEBUG_MODE:
                logger.success(f'File found: {file_path} -> {file}')
                return cvimage
        else:
            if self.settings.DEBUG_MODE:
                logger.error(f'File found: {file_path} -> {file}')
            return None

    def create_all_data(self):
        """
        Create all data by calling the `_create_entities` method with different parameters.

        :return: A tuple containing three values: `sf` - the result of `_create_entities` with `ContainerType.SAFE_ZONE`,
                 `gw` - the result of `_create_entities` with `ContainerType.GAME_WINDOW`,
                 and `bf` - the result of `_create_entities` with `ContainerType.BUFFS`.
        """
        sf = self._create_entities(images=safe_zone_images,
                                   corners=safe_zone_corners,
                                   offsets=safe_zone_offset,
                                   entity_type=ContainerType.SAFE_ZONE,
                                   )
        gw = self._create_entities(images=game_window,
                                   corners=None,
                                   offsets=None,
                                   entity_type=ContainerType.GAME_WINDOW,
                                   )
        bf = self._create_entities(images=buffs,
                                   corners=buffs_corner,
                                   offsets=buffs_offset,
                                   entity_type=ContainerType.BUFFS,
                                   )

        return sf, gw, bf

    @staticmethod
    def create_safe_zones_names():
        """
        Creates a list of safe zone names.

        Returns:
            list: A list of safe zone names.
        """
        return [item for item in safe_zone_images.keys()]
