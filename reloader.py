# Overview -  This script is to automate reloading of QT app when we make any changes in the python code file. This will
# reduce the overhead of restarting application again and again written by Nahar


# // Please note user with caution as this script may consume continuos system ram resources



import sys
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Detected change in {event.src_path}. Restarting...")
            self.start_process()

if __name__ == "__main__":
    path = "."  # Isme  mention out directory where u need to monitor changes
   #  command = "python designer_file.py" This should be our project main file

    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()