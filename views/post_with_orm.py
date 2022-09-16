from flask import render_template, request, flash, url_for
from flask import Blueprint, abort, redirect
from model import Posts
from settings import db


from flask_login import login_required


post = Blueprint('posts', __name__)


@post.route('/')
def main():
    posts_ = Posts.query.all()
    return render_template('main.html', posts=posts_)


@post.route('/post/<int:post_id>')
def show_post(post_id):
    post_ = Posts.query.filter_by(id=post_id).first()
    if post_ is None:
        abort(404)
    return render_template('post.html', post=post_)


@post.route('/post/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!')
        else:
            post_ = Posts(title=title, content=content)
            db.session.add(post_)
            db.session.commit()
            return redirect(url_for('posts.main'))
    return render_template('create.html')


@post.route('/other')
def other():
    return render_template('other.html')


@post.route('/post/edit/<int:post_id>', methods=('GET', 'POST'))
@login_required
def edit_post(post_id):
    post_ = Posts.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        post_.title = request.form['title']
        post_.content = request.form['content']

        if not post_.title:
            flash('Укажите заголовок!')
        else:
            db.session.add(post_)
            db.session.commit()
            return redirect(url_for('posts.show_post', post_id=post_id))

    return render_template('edit.html', post=post_)


@post.route('/post/delete/<int:post_id>', methods=('POST',))
@login_required
def delete_post(post_id):
    post_ = Posts.query.filter_by(id=post_id).first()
    db.session.delete(post_)
    db.session.commit()
    flash(f'"{post_.title}" был успешно удалён!')
    return redirect('/')








