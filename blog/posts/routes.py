from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import current_user, login_required

from blog import db
from blog.posts.forms import PostForm
from blog.models import Post

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        created_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(created_post)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post ', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    requested_post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=requested_post.title, post=requested_post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    updated_post = Post.query.get_or_404(post_id)
    if updated_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        updated_post.title = form.title.data
        updated_post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = updated_post.title
        form.content.data = updated_post.content
    return render_template('create_post.html', title=updated_post.title, form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    deleted_post = Post.query.get_or_404(post_id)
    if deleted_post.author != current_user:
        abort(403)
    db.session.delete(deleted_post)
    db.session.commit()
    flash('Your post has been successfully deleted!', 'success')
    return redirect(url_for('main.home'))
