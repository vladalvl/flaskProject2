import sqlite3
from flask import render_template, request, url_for, flash, redirect, abort
from flask import Blueprint


posts_bp = Blueprint('posts', __name__)


def get_db_connection():
    """Подключение к DB"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@posts_bp.route('/')
def main():
    """Показывает все посты, главная страница"""
    conn = get_db_connection()
    posts = conn.execute(f'SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('main.html', posts=posts)


@posts_bp.route('/<int:post_id>')
def show_post(post_id):
    """Показывает пост по его ID """
    conn = get_db_connection()
    post = conn.execute(f'SELECT * FROM posts WHERE id={post_id}').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return render_template('post.html', post=post)


@posts_bp.route('/create', methods=('GET', 'POST'))
def create_post():
    """Добавление нового поста"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!')
        if not content:
            flash('Укажите содержание поста!')

        if content and title:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main'))
    return render_template('create.html')


@posts_bp.route('/other')
def other():
    """ """
    return render_template('other.html')


@posts_bp.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit_post(post_id):
    """Редактирование поста"""
    conn = get_db_connection()
    post = conn.execute(f'SELECT * FROM posts WHERE id={post_id}').fetchone()
    conn.close()
    if post is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!')
        if not content:
            flash('Укажите содержание поста!')

        if title and content:
            conn = get_db_connection()
            conn.execute(f'UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('show_post', post_id=post_id))

    return render_template('edit.html', post=post)


@posts_bp.route('/<int:post_id>/delete', methods=('POST',))
def delete_post(post_id):
    """Удаление поста"""
    conn = get_db_connection()
    post = conn.execute(f'SELECT * FROM posts WHERE id={post_id}').fetchone()
    conn.close()
    if post is None:
        abort(404)

    conn = get_db_connection()
    conn.execute(f'DELETE FROM posts WHERE id={post_id}')
    conn.commit()
    conn.close()
    flash(f'"{post["title"]}" был успешно удалён!')
    return redirect(url_for('main'))
