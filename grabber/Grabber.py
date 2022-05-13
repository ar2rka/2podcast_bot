from abc import ABC, abstractmethod


class Grabber(ABC):
    def __init__(self, source):
        self.source = source
        self.conn = None

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass
