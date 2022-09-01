from . import api
from flask import jsonify, request
from app.models import Post, User


@api.route('/')
def index():
    names = ['Brian', 'Tatyana', 'Nate', 'Sam']
    return jsonify(names)


@api.route('/posts', methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=["POST"])
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    print(data, type(data))
    # Validate the data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if field not in request body, respond with a 400 error
            return jsonify({'error': f"{field} must be in request body"}), 400
    
    # Get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # Create new instance of post with data
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict_users() for u in users])


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict_users())




@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({'error': f" {field} must be in request body"})


    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict_users()), 201