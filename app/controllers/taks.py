from app import db
from app.models.task import TaskForm, Task
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

task_route = Blueprint("tasks", __name__)


"""     ROTAS A SEREM ADICIONADAS 

        * /tasks/ (get) - faz o carregamento de todas as tarefas existestes, haverá filtro entre
                          as tarefas pendentes e já concluídas;
        * /tasks/create (GET) - carrega o formulário para criação de tarefas;
        * /tasks/create (POST) - faz  o envio das informações inseridas;
        * /tasks/id (get) - carregamento de uma tarefa;
        * /tasks/id/completed (PUT) - alterar o status de pendent True(1) para False (0);
        * /tasks/id/update (get) - carregamento de formulário para alterações;
        * /tasks/id/update (PUT) - envio de alterações realizadas;
        * /tasks/id/delete (DELETE) - realizar exclusão de tarefa;;

"""


@task_route.route('/home')
@login_required
def home():
    tasks_pendent = Task.query.filter_by(user_id=current_user.id, pendent=1).all()
    tasks_completed = Task.query.filter_by(user_id=current_user.id, pendent=0).all()
    print(tasks_pendent)
    print(tasks_completed)
    return render_template('tasks/read.html', tasks=tasks_pendent)


@task_route.route('/<id>', methods=['PUT'])
@login_required
def completed(id):
    if Task.query.filter_by(id=id).first():
        task = Task.query.filter_by(id=id).first()
        if task.pendent == 1:
            task.pendent = 0
            db.session.commit()
            flash(f'Tarefa foi concluida com sucesso!')
            return jsonify(status='completed')
        else:
            flash(f'Tarefa já está concluida!')
            return jsonify(status='already-completed')

    else:
        return jsonify(status='not-completed')


@task_route.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TaskForm()
    if form.is_submitted():
        new_task = Task(form.title.data, form.content.data, user_id=current_user.id)
        print(new_task)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks.home'))
    return render_template('tasks/create.html', form=form)


@task_route.route('/<id>')
@login_required
def read_task(id):
    if Task.query.filter_by(id=id).first():
        task = Task.query.filter_by(id=id).first()
        return render_template('tasks/read-task.html', task=task)
    else:
        flash("Nenhum tarefa encontrada!")
        return redirect(url_for('tasks.home'))
    

@task_route.route('/<id>/update', methods=['GET'])
@login_required
def update_form(id):
    if Task.query.filter_by(id=id).first():
        task = Task.query.filter_by(id=id).first()
        return render_template('tasks/update-task.html', task=task)
    else:
        flash(f"Tarefa de id '{id}' não encontrada!")
        return redirect(url_for('tasks.home'))



@task_route.route('/<id>/update', methods=['PUT'])
@login_required
def update_put(id):
    task_update = request.json
    task = Task.query.filter_by(id=id).first()
    task.title = task_update['title']
    task.content = task_update['content']
    db.session.commit()
    
    return jsonify(status='ok', url=url_for('tasks.read_task', id=id))
