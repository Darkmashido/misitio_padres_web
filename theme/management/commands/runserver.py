import os
import subprocess
import sys

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    """runserver que levanta tambien el watcher de Tailwind."""

    def run(self, **options):
        watcher = None
        # RUN_MAIN lo define el autoreloader en el proceso hijo; el watcher se lanza una sola vez.
        if settings.DEBUG and os.environ.get("RUN_MAIN") != "true":
            watcher = subprocess.Popen([sys.executable, "manage.py", "tailwind", "start"])
        try:
            super().run(**options)
        finally:
            if watcher:
                watcher.terminate()
