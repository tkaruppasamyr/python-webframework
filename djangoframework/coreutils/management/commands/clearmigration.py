import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear all migration files'

    def handle(self, *args, **options):

        confirm = input(
            "Are you sure? This will delete all migration files (yes/no): "
        )
        if confirm.lower() not in ["yes", "y","yes"]:
            self.stdout.write("Cancelled.")
            return

        base_dir = os.getcwd()
        deleted_files = []
        
        for root, dirs, files in os.walk(base_dir):
            if "migrations" in root:
                for file in files:
                    if file.endswith(".py") or file.endswith(".pyc"):
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        deleted_files.append(file_path)
        
        self.stdout.write(self.style.SUCCESS( f"Deleted {len(deleted_files)} migration files"))