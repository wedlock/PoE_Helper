from threading import Thread, Lock
from abc import ABC, abstractmethod


class ThreadBase(ABC):
    @abstractmethod
    def __init__(self):
        self.lock = Lock()
        self.stopped = True

    @abstractmethod
    def is_stopped(self):
        return self.stopped

    @abstractmethod
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    @abstractmethod
    def run(self):
        pass
        # while not self.stopped:
        #     self.lock.acquire()
        #     self.lock.release()

    @abstractmethod
    def stop(self):
        self.stopped = True

    @abstractmethod
    def update(self, screenshot):
        pass
        # self.lock.acquire()
        # self.lock.release()
