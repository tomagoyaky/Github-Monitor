import time
from django.core.management.base import BaseCommand
from django.db.models import Q
from multiprocessing import Process
from github_monitor.apps.monitor.models.task import Task
from github_monitor.apps.monitor.processors import TaskProcessor


class Command(BaseCommand):

    task_id_list = []
    INTERVAL = 5

    def handle(self, *args, **options):

        def _process(_processor):
            _processor.process()

        while True:
            for task in Task.objects.filter(~Q(id__in=self.task_id_list)):
                processor = TaskProcessor(task)
                p = Process(target=_process, args=(processor, ))
                p.start()
                self.task_id_list.append(task.id)
            time.sleep(self.INTERVAL)