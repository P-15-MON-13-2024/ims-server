#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading


def start_telegram_bot():
    from imsserver.utils import run_telegram_bot
    run_telegram_bot()
    


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imsserver.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    thread = None
    if 'runserver' in sys.argv:
        thread = threading.Thread(target=start_telegram_bot)
        thread.start()

    execute_from_command_line(sys.argv)

    return thread 


if __name__ == '__main__':
    thread = main()
    if thread:
        thread.join()


