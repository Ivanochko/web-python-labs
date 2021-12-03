from flask import url_for, render_template, redirect,\
    flash, abort, current_app
from flask_login import login_required
from .models import Post
from .. import db, App
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from .form import PostForm

from . import post_blueprint
from PIL import Image


@post_blueprint.route('/')
def index():
    posts = Post.query.all()
    image = url_for('static', filename='post_pics')
    return render_template('index.html', posts=posts,
                           image=image, menu=App.getMenu())


@post_blueprint.route('/<postId>', methods=['GET', 'POST'])
def view(postId):
    post = Post.query.get_or_404(postId)
    image = url_for('static', filename='post_pics/' + post.image)
    return render_template('post.html', post=post,
                           menu=App.getMenu(), image=image)


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
        else:
            image = 'default_post.png'

        post = Post(title=form.title.data,
                    description=form.description.data,
                    type=form.type.data,
                    image=image,
                    user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('post.index'))

    return render_template('create_post.html', form=form, menu=App.getMenu())


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static\\post_pics', picture_fn)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@post_blueprint.route('/<postId>/delete', methods=['GET', 'POST'])
def delete_post(postId):
    post = Post.query.get_or_404(postId)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.index'))

    flash('Post is not yours', category='warning')
    return redirect(url_for('post.view', postId=postId))


@post_blueprint.route('/<postId>/update', methods=['GET', 'POST'])
def update_post(postId):
    post = Post.query.get_or_404(postId)
    if current_user.id != post.user_id:
        flash('Post is not yours', category='warning')
        return redirect(url_for('post.view', post=post))

    form = PostForm()

    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            post.image = image

        post.title = form.title.data
        post.description = form.description.data
        post.type = form.type.data

        db.session.commit()
        db.session.add(post)

        flash('The post has been updated', category='success')
        return redirect(url_for('post.view', postId=post.id))

    form.title.data = post.title
    form.description.data = post.description
    form.type.data = post.type

    return render_template('update_post.html', form=form, menu=App.getMenu())
