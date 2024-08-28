from app import db
from app.models.task import TaskForm, Task
from app.controllers.decorators import email_confirmation_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, json
from flask_login import login_required, current_user

task_route = Blueprint("tasks", __name__)


"""     ROTAS A SEREM ADICIONADAS 

OK        * /tasks/ (get) - faz o carregamento de todas as tarefas existestes, haverá filtro entre
                          as tarefas pendentes e já concluídas;
OK        * /tasks/create (GET) - carrega o formulário para criação de tarefas;
OK        * /tasks/create (POST) - faz  o envio das informações inseridas;
OK        * /tasks/id (get) - carregamento de uma tarefa;
OK        * /tasks/id/completed (PUT) - alterar o status de pendent True(1) para False (0);
OK        * /tasks/id/update (get) - carregamento de formulário para alterações;
OK        * /tasks/id/update (PUT) - envio de alterações realizadas;
OK        * /tasks/id/delete (DELETE) - realizar exclusão de tarefa;;

"""


@task_route.route('/home')
@login_required
def home():
    page = request.args.get('page', default=1, type=int)
    per_page = 9

    tasks = Task.query.filter_by(user_id=current_user.id, pendent=True).paginate(page=page, per_page=per_page)
    pages = tasks.pages
    
    return render_template('tasks/read.html', tasks=tasks)


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


@task_route.route('/<id>/delete', methods=['DELETE'])
@login_required
def delete(id):
    task_to_delete = Task.query.filter_by(id=id).first()
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except Exception as erro:
        return jsonify(erros=erro)
    else:
        return jsonify(status='ok', url=url_for('tasks.home'))
