from app import db
from flask import Blueprint, render_template

task_route = Blueprint("tasks", __name__)


@task_route.route('/create')
def create_form():
    # form = TaskForm()
    return render_template('tasks/create.html')

@task_route.route('/create', methods=['POST'])
def create_post():
    # form = TaskForm()
    pass