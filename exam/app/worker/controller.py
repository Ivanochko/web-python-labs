from flask import url_for, render_template, redirect,\
    flash, current_app
from flask_login import login_required
from .models import Worker, Grade
from .. import db, App
from .form import WorkerForm, GradeForm

from . import worker_blueprint


@worker_blueprint.route('/')
def index():
    workers = Worker.query.order_by(Worker.hired_at.desc())
    return render_template('workers.html', workers=workers,
                           menu=App.getMenu())


@worker_blueprint.route('/<workerId>', methods=['GET', 'POST'])
def view(workerId):
    worker = Worker.query.get_or_404(workerId)
    return render_template('worker.html', worker=worker,
                           menu=App.getMenu())


@worker_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = WorkerForm()
    grades = Grade.query.all()

    form.grade.choices = [(grade.id, grade.name)
                          for grade in grades]

    if form.validate_on_submit():
        worker = Worker(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        surname=form.surname.data,
                        address=form.address.data,
                        email=form.email.data,
                        mobile=form.mobile.data,
                        salary=form.salary.data,
                        hired_at=form.hired_at.data,
                        grade_id=form.grade.data)

        db.session.add(worker)
        db.session.commit()

        return redirect(url_for('worker.index'))

    return render_template('create_worker.html', form=form, menu=App.getMenu())


@worker_blueprint.route('/<workerId>/delete', methods=['GET', 'POST'])
def delete_worker(workerId):
    worker = Worker.query.get_or_404(workerId)
    db.session.delete(worker)
    db.session.commit()
    flash('Worker ' + worker.first_name + ' '
          + worker.last_name + ' was deleted')
    return redirect(url_for('worker.index'))


@worker_blueprint.route('/<workerId>/update', methods=['GET', 'POST'])
def update_worker(workerId):
    worker = Worker.query.get_or_404(workerId)
    form = WorkerForm()
    grades = Grade.query.all()

    form.grade.choices = [(grade.id, grade.name)
                          for grade in grades]

    if form.validate_on_submit():
        worker.first_name = form.first_name.data
        worker.last_name = form.last_name.data
        worker.surname = form.surname.data
        worker.address = form.address.data
        worker.email = form.email.data
        worker.mobile = form.mobile.data
        worker.salary = form.salary.data
        worker.hired_at = form.hired_at.data
        worker.grade_id = form.grade.data

        db.session.commit()

        flash('Worker data has been updated', category='success')
        return redirect(url_for('worker.view', workerId=worker.id))

    form.grade.data = worker.grade_id
    form.grade.default = worker.grade_id
    form.process()
    form.first_name.data = worker.first_name
    form.last_name.data = worker.last_name
    form.surname.data = worker.surname
    form.address.data = worker.address
    form.email.data = worker.email
    form.mobile.data = worker.mobile
    form.salary.data = worker.salary
    form.hired_at.data = worker.hired_at
    return render_template('update_worker.html', form=form,
                           menu=App.getMenu(), worker=worker)


@worker_blueprint.route('/grades', methods=['GET', 'POST'])
def categories():
    form = GradeForm()
    if form.name.data:
        grade = Grade(name=form.name.data)
        db.session.add(grade)
        db.session.commit()
        form.name.data = ''
        flash('Grade ' + grade.name + ' added!', category='success')
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades,
                           form=form, menu=App.getMenu())


def get_grade_name(id):
    return Grade.query.get(id).name


current_app.jinja_env.globals.update(get_grade_name=get_grade_name)
