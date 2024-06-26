from . import api
from ..models import Post, db, User
from flask import request
from werkzeug.security import check_password_hash
import base64
from ..apiauthhelper import token_auth_required, basic_auth, basic_auth, token_auth

@api.get('/posts')
def get_all_posts_API():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    user = None
    if "Authorization" in request.headers:
            val = request.headers['Authorization']
            type, token = val.split()
            if type == "Bearer":
                token = token
                user = User.query.filter_by(token=token).first()
    return {
        'status' : 'ok',
        'results' : len(posts),
        'posts' : [p.to_dict(user) for p in posts]
    }, 200


@api.get('/posts/<post_id>')
def get_a_post_API(post_id):
    post = Post.query.get(post_id)
    user = None
    if "Authorization" in request.headers:
            val = request.headers['Authorization']
            type, token = val.split()
            if type == "Bearer":
                token = token
                user = User.query.filter_by(token=token).first()
    if post:
        return {
            'status' : 'ok',
            'results' : 1,
            'post' : post.to_dict(user)
        }, 200
    return {
        'status' : 'not ok',
        'message' : 'The post you are looking for does not exist.'
    }, 404

@api.post('/post/create')
@token_auth_required
def create_post_api(user):

    try:

        data = request.json

        title = data['title']
        img_url = data['img_url']
        caption = data.get('caption', '')

        post = Post(title, caption, img_url, user.id)

        db.session.add(post)
        db.session.commit()

        return {
            'status' : 'ok',
            'message' : 'Successfully created a post!'
        }, 201
    except:
        return {
            'status' : 'Not ok',
            'message' : 'Not enough info provided to create a post.'
        }, 400
    
@api.post('/posts/like/<post_id>')
@token_auth_required
def like_post_API(post_id, user):
    post = Post.query.get(post_id)

    if post:
        user.liked_posts2.append(post)
        db.session.commit()
    return {
        "status" : "ok",
        "message" : "You have successfully liked the post!"
    }

@api.post('/posts/unlike/<post_id>')
@token_auth.login_required
def unlike_post_API(post_id):
    user = token_auth.current_user()
    post = user.liked_posts2.filter_by(id=post_id).first()
    if post:
        user.liked_posts2.remove(post)
        db.session.commit()
    return {
        "status" : "ok",
        "message" : "You have successfully unliked the post!"
    }

@api.post('/signup')
def sign_up_API():
    try:

        data = request.json

        username = data['username']
        email = data['email']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            return {
                'status' : 'Not ok',
                'message' : 'Username is taken.'
            }, 400
        user = User.query.filter_by(email=email).first()
        if user:
            return {
                'status' : 'Not ok',
                'message' : 'Email is taken.'
            }, 400
        

        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        return {
            'status' : 'ok',
            'message' : 'Successfully created your user!'
        }, 201
    except:
        return {
            'status' : 'Not ok',
            'message' : 'Not enough info provided to create your user.'
        }, 400

@api.post('/login')
@basic_auth.login_required

def login_API():
            user = basic_auth.current_user()
            return {
                'status' : 'ok',
                'user' : user.to_dict(),
                'message' : 'Successfully logged in!'
            }, 200
