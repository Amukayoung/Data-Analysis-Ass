from django.core.management.base import BaseCommand
from danalysis.Scripts.workerScript import processWorkerData


class Command(BaseCommand):
    help = "Process file and save worker details to the database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        result = processWorkerData(file_path)
        self.stdout.write(self.style.SUCCESS(result))
