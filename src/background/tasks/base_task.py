from abc import ABCMeta, abstractmethod


class BaseTask(metaclass=ABCMeta):
    @abstractmethod
    async def run(self):
        raise NotImplementedError
