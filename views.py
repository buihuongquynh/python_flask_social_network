from operator import le
from flask import Blueprint, render_template, request
from flask.helpers import flash
from flask_login import login_user, login_required, logout_user, current_user
from models import Post, User
from initial import db

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post) < 1:
            flash('post is too short!', category='error')
        else:
            new_post = Post(body = post, author_id = current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post is created!', category='success')
    return render_template('home.html', user= current_user, posts= current_user.posts)