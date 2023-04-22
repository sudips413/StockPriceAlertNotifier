from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_cors import CORS

from flask import Blueprint
from routes.home import blueprint as home

app = Flask(__name__,static_folder='static')

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(home)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Do something when a file is modified
        print("File modified")

if __name__ == '__main__':
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    app.run(debug=True)
