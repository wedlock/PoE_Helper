from threading import Thread, Lock
from time import sleep

from health import Health
from thread_base import ThreadBase


class Information(ThreadBase):
    def is_stopped(self):
        """
        Check if the object is stopped.

        Returns:
            bool: True if the object is stopped, False otherwise.
        """
        return self.stopped

    def __init__(self, player_hp: Health.get_hp, fps_values: list,
                 sleep_time: float = 1):
        """
        Initializes the class instance.

        Parameters:
            player_hp (Health.get_hp): The method to get the player's health points.
            fps_values (list): A list of FPS values.
            sleep_time (float, optional): The time to sleep between iterations. Defaults to 1.

        Returns:
            None
        """
        self.stopped = True
        self.safezone = None
        self.lock = Lock()
        self.fps_values = fps_values
        self.get_player_hp = player_hp
        self.sleep_time = sleep_time

    def start(self):
        """
        Start the function execution.

        This function starts the execution of the thread by setting the `stopped` attribute to `False`
        and creating a new thread to run the `run` method.

        """
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def run(self):
        """
        Runs the function in an infinite loop until the `self.stopped` flag is set to True.

        This function continuously retrieves the FPS values from the `self.fps_values` list.
        It then acquires a lock to access the player's current and maximum HP values.
        After releasing the lock, it checks if the safezone flag is set and assigns
        a string value to the `safe` variable accordingly.

        If the player's current and maximum HP values are not available, it sets them to 0.

        The function then constructs a text string using the `safe` value,
         the player's current and maximum HP values, and the FPS values.
        The constructed text is printed on the console without a new line character,
         effectively updating the output on the same line.

        The function pauses execution for the specified sleep time before repeating the loop.
        """

        while not self.stopped:
            fps_method = []
            for get_fps in self.fps_values:
                fps_method.append(get_fps())
            self.lock.acquire()

            current_hp, max_hp = self.get_player_hp()
            self.lock.release()
            safe = None

            if self.safezone is not None:
                if self.safezone:
                    safe = "TRUE"
                else:
                    safe = "FALSE"

            if current_hp is None and max_hp is None:
                current_hp, max_hp = 0, 0

            text = (
                f"Safe zone: {safe} "
                f"Health: {current_hp}/{max_hp}"
                f" fps: {fps_method}")
            print("\r{0}".format(text), end="")
            sleep(self.sleep_time)

    def stop(self):
        """
        Stops the function.

        No parameters.

        No return value.
        """
        self.stopped = True

    def update(self, safezone):
        """
        Update the safezone value.

        Parameters:
            safezone (bool): The new value for safezone.

        Returns:
            None
        """
        self.lock.acquire()
        self.safezone = safezone
        self.lock.release()
        pass
