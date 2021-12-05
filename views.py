import os
from flask import Blueprint, render_template, request, redirect
from flask.helpers import flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from models import Post, User
from initial import db
from werkzeug.utils import secure_filename  

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if request.method == 'POST':
        post = request.form.get('post')
        pic = request.files['image']
        picdata = ""
        if not pic:
            picdata = ""
        else:
            filename = secure_filename(pic.filename)
            pic.save(os.path.join("D:\Python_File\python_flask_social_network\static",filename))
            picdata = filename
        if len(post) < 1:
            flash('post is too short!', category='error')
        else:
            new_post = Post(body = post, author_id = current_user.id, img = picdata)
            db.session.add(new_post)
            db.session.commit()
            flash('Post is created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('home.html', user= current_user, posts= posts)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/edit-post/<id>", methods = ['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to delete this post.', category='error')
    elif request.method == 'POST':
        body = request.form.get('post')
        pic = request.files['image']
        picdata = ""
        if not pic:
            picdata = ""
        else:
            filename = secure_filename(pic.filename)
            pic.save(os.path.join("D:\Python_File\python_flask_social_network\static",filename))
            picdata = filename
        if len(body) < 1:
            flash('post is too short!', category='error')
        else:
            # new_post = Post(body = body, author_id = current_user.id, img = picdata)
            post.body = body
            post.img = picdata
            # db.session.add(new_post)
            db.session.commit()
            flash('Post is updated!', category='success')
            return redirect(url_for('views.home'))
    return render_template('edit-post.html', user= current_user, post= post)



@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
