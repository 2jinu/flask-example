import psutil
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required

from my_app import sock
from my_app.models.role import role_required

from threading import Lock
thread = None
thread_lock = Lock()

bp_dashboard = Blueprint(name="dashboard", import_name=__name__, url_prefix="/dashboard/", template_folder="templates/admin")

def server_resource():
    current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cpu = psutil.cpu_percent(interval=5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(path="/")

    resource = dict(
        current=current,
        cpu=cpu,
        memory=dict(
            used=round(memory.used / (1024 ** 3), 2),
            total=round(memory.total / (1023 ** 3), 2)
        ),
        disk=dict(
            used=round(disk.used / (1024 ** 3), 2),
            total=round(disk.total / (1024 ** 3), 2)
        )
    )
    return resource

def background_thread():
    while True:
        sock.emit("updateResource", server_resource())

@bp_dashboard.route(rule="/", methods=["GET"])
@login_required
@role_required(["ADMIN"])
def main():
    return render_template(
        template_name_or_list="admin/dashboard.html"
    )

@sock.on(message="connect")
@login_required
@role_required(["ADMIN"])
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = sock.start_background_task(background_thread)