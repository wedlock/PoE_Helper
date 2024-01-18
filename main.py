from multiprocessing import Value
from time import sleep

import keyboard
from loguru import logger
from pywinauto import Application, ElementNotFoundError

from Helpers import execute_game
from detect import Detection
from health import Health
from info import Information
from keyboard_thread import KeysToPress
from screenshot import Screenshot
from settings import Settings


# OCR_OPTIONS = r'--psm 7 --oem 3 digit=1234567890'

# GAME_CORNER = [0, 0]

# Pause_Thread = False

# Press_key_e_semaphore = Value('b', False, lock=False)
# Press_key_1_semaphore = Value('b', False, lock=False)
# Panic_flask_semaphore = Value('b', False, lock=False)

# PATTERNS = []
#
# BLOCKING_HP_READ = ["OPTIONS", "SOCJAL", "CHARACTER"]

# Max_Health = 0
# Current_Health = 0

def set_focus(window_name: str):
    """
    Sets the focus to a window with the given name.

    Args:
        window_name (str): The name of the window to set focus to.

    Returns:
        bool: True if the focus was successfully set, False otherwise.
    """
    try:
        app = Application().connect(title=window_name)
    except ElementNotFoundError:
        if Settings.DEBUG_MODE:
            logger.warning(f'No window with name {window_name} found')
        return False
    w = app.window(title=window_name)
    w.set_focus()
    return True


def initialize_variables():
    """
    Initializes variables and returns threads and th_list.
    """
    from Helpers.threads_holder import BotThreads
    th_list = []
    threads = BotThreads()

    threads.screenshot = Screenshot(settings=settings, game_window_name=settings.GAME_WINDOW_NAME)
    th_list.append(threads.screenshot)

    threads.detect = Detection(settings=settings, patterns=settings.TO_FIND_IN_SCREEN,
                               ss_method=threads.screenshot.get_screenshot)
    th_list.append(threads.detect)
    threads.health = Health(settings=settings, ss_method=threads.screenshot.get_screenshot)
    th_list.append(threads.health)

    fps_values = [threads.detect.get_fps, threads.health.get_fps, threads.screenshot.get_fps]

    threads.info = Information(threads.health.get_hp, fps_values, sleep_time=0.5)
    th_list.append(threads.info)

    threads.key_e = KeysToPress(settings=settings, key=('e',), delay_after_stop=18)
    th_list.append(threads.key_e)

    threads.key_r = KeysToPress(settings=settings, key=('r',), delay_after_stop=8.5)
    th_list.append(threads.key_r)

    threads.key_w = KeysToPress(settings=settings, key=('w',), delay_after_stop=19,
                                buffs_list=threads.detect.get_matches, buff_to_watch="HASTE")
    th_list.append(threads.key_w)

    threads.key_1 = KeysToPress(settings=settings, key=('1',), delay_after_stop=5)
    th_list.append(threads.key_1)

    threads.key_panic = KeysToPress(settings=settings, key=('2', '3', '4', '5'), delay_after_stop=5)
    th_list.append(threads.key_panic)



    return threads, th_list


def try_run_game():
    """
    Execute the game by creating an instance of the `execute_game.ExecuteGame` class with the provided `settings` and calling its `run` method.

    Parameters:
        None

    Returns:
        None
    """
    exe = execute_game.ExecuteGame(settings)
    exe.run()

"""
The main entry point of the program.

This function initializes settings, variables, and threads, and runs the game. It also handles key presses and controls the botting behavior based on health and safe zones.

Returns:
    None
"""
if __name__ == '__main__':
    pause = False
    settings = Settings()
    settings.initialize()
    threads, threads_list = initialize_variables()
    try_run_game()

    set_focus(settings.GAME_WINDOW_NAME)


    threads.screenshot.start()

    threads.detect.start()

    threads.health.start()

    threads.info.start()

    sleep(1)



    threads.key_r.start()
    threads.key_w.start()
    while True:


        if (keyboard.is_pressed(settings.EXIT_SHORTCUT[0])
                and keyboard.is_pressed(settings.EXIT_SHORTCUT[1])):
            if settings.DEBUG_MODE:
                logger.info(f'Exit shortcut pressed, exiting from botting')
            for thread in threads_list:
                thread.stop()
                if settings.DEBUG_MODE:
                    logger.info(f'Stopping {thread}')
            quit(0)

        if keyboard.is_pressed('spacebar'):

            pause = not pause
            while keyboard.is_pressed('spacebar'):
                continue
                pass
            if pause:
                if settings.DEBUG_MODE:
                    logger.info('Pausing bot')
            else:
                if settings.DEBUG_MODE:
                    logger.info('Resuming bot')

        if not pause:

            Health = threads.health.get_hp()
            try:
                current_health = int(Health[0])
            except ValueError:
                current_health = 0
            try:
                max_health = int(Health[1])
            except ValueError:
                max_health = 0
            health_percent = 100
            if max_health > 0:
                health_percent = int((current_health / max_health) * 100)

            safe = threads.detect.get_matches()

            auto_pause_botting = None

            for item in safe:
                if item in settings.SAFE_ZONES:
                    auto_pause_botting = True
                    threads.info.update(auto_pause_botting)
                    break
                else:
                    auto_pause_botting = False
                    threads.info.update(auto_pause_botting)

            if not auto_pause_botting:
                if threads.key_e.is_stopped() and threads.key_w.is_stopped():
                    if not keyboard.is_pressed('ctrl'):
                        threads.key_w.start()
                if threads.key_r.is_stopped():
                    if not keyboard.is_pressed('ctrl'):
                        threads.key_r.start()

            if health_percent <= 90:
                if not auto_pause_botting:
                    threads.key_w.stop()
                    if threads.key_e.is_stopped():
                        if settings.DEBUG_MODE:
                            logger.info(f'Health below 90% {current_health}/{max_health}. Using key e')
                        threads.key_e.start()

            if health_percent <= 70:
                if not auto_pause_botting:
                    if threads.key_1.is_stopped():
                        if settings.DEBUG_MODE:
                            logger.info(f'Health below 70% {current_health}/{max_health}. Using key 1')
                        threads.key_1.start()

            if health_percent <= 50:
                if not auto_pause_botting:
                    if threads.key_panic.is_stopped():
                        if settings.DEBUG_MODE:
                            logger.info(f'Health below 50% {current_health}/{max_health}. Using panic key')
                        threads.key_panic.start()





