from operator import le
from flask import Blueprint, render_template, request
from flask.helpers import flash
from flask_login import login_user, login_required, logout_user, current_user
from models import Post, User
from initial import db

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post) < 1:
            flash('post is too short!', category='error')
        else:
            new_post = Post(body = post, author_id = current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post is created!', category='success')
    return render_template('home.html', user= current_user, posts= posts)

@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
