from flask import render_template, request, redirect, url_for
from app import app
from .forms import SignUpForm, LoginForm, SignUpForm, PostForm
from .models import User, db, Post
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/contact')
def contact_page():
    return render_template('contact.html')


## Authentication
@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            #Find user from database

            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    print('Incorrect pass')
            else:
                print('That username doesnt exist')

        
    return render_template('login.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            #Adds user to database
            return redirect(url_for('login_page'))

    return render_template('signup.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

## POSTS
@app.route('/posts/create', methods = ["GET", "POST"])
@login_required
def create_post_page():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title=form.title.data
            caption=form.caption.data
            img_url=form.img_url.data

            my_post = Post(title, caption, img_url, current_user.id)

            db.session.add(my_post)
            db.session.commit()

            return redirect(url_for('home_page'))

    return render_template('createpost.html', form = form)

@app.route('/')
@app.route('/posts')
def home_page():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/posts/<post_id>')
def single_post_page(post_id):
    post = Post.query.filter_by(id = post_id).first() # these two are identical
    #post = Post.query.get(post.id)
    if post:
        return render_template('singlepost.html', post=post)
    else:
        return redirect(url_for('home_page'))
    
@app.route('/posts/update/<post_id>', methods=["GET", "POST"])
@login_required
def update_post_page(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home_page'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title=form.title.data
            caption=form.caption.data
            img_url=form.img_url.data

            post.title = title
            post.caption = caption
            post.img_url = img_url

            db.session.commit()
            return redirect(url_for('single_post_page', post_id = post.id))

    return render_template('updatepost.html', post=post, form=form)

@app.route('/posts/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home_page'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home_page'))