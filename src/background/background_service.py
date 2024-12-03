from typing import List
from .tasks import BaseTask


# It should be used if you have multiple background tasks to run, it is not necessary if you have only one task.
class BackgroundService:
    def __init__(
        self,
        tasks: List[BaseTask],
        # we can set an async scheduler and run multiple routines as needed
        # routines: List[BaseRoutine],
    ):
        self.tasks = tasks

    async def start(self):
        for task in self.tasks:
            await task.run()
