from datetime import datetime
import os
from sys import version

from flask import render_template, request, flash, session

from app.forms import LoginFormSecond, LoginForm
from app.file_writer import writeToFile
from app import app, App
from app.custom_validator import validate


@app.route('/form_second', methods=['GET', 'POST'])
def form_second():
    form = LoginFormSecond()
    validate(form=form)

    if form.validate_on_submit():
        writeToFile(form)
        flash('User has been written in json file')
        session['login'] = form.login.data
        session['e_l_number'] = form.e_l_number.data
        return render_template("result.html",
                               form=form,
                               menu=App.getMenu())

    return render_template("form_second.html",
                           login=session['login'],
                           e_l_number=session['e_l_number'],
                           form=form,
                           menu=App.getMenu())


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    REPORT_MESS = '<h1>The username is {}. The password is {}</h1>'
    if form.validate_on_submit():
        return REPORT_MESS.format(form.username.data, form.password.data)
    return render_template("form.html",
                           form=form,
                           menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route('/')
def index():
    return render_template("main.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route("/about")
def about():
    return render_template("about.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/achievements")
def score():
    return render_template("achievements.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))