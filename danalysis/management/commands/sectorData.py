from django.core.management.base import BaseCommand
from danalysis.sectorScript import processSectorData


class Command(BaseCommand):
    help = "Process file and save sector details to the database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        result = processSectorData(file_path)
        self.stdout.write(self.style.SUCCESS(result))
