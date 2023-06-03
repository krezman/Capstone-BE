import models

from flask import Blueprint, request, jsonify

# there are some useful tools that come with peewee
from playhouse.shortcuts import model_to_dict

#login stuffs!
from flask_login import login_required, current_user

posts = Blueprint('posts', 'posts')

@posts.route('/index', methods=['GET'])
def post_index():
    results = models.Post.select()
    post_dicts = [model_to_dict(post) for post in results]

    for post_dict in post_dicts:
        post_dict['post_owner'].pop('password')

        return jsonify({
            'data': post_dicts,
            'message': "Successfully found posts!!",
            'status': 200
        }), 200

@posts.route ('/create', methods=['POST'])
def create_post():
    payload = request.get_json()

    new_post = models.Post.create(photo = payload['photo'], text = payload['text'], post_owner = payload['id'])

    post_dict = model_to_dict(new_post)

    post_dict['post_owner'].pop('password')

    return jsonify(
        data = post_dict,
        message = f'Successfully create a new post by {current_user}',
        status = 201
    ), 210


@posts.route('/<id>', methods=['GET'])
def get_one_post(id):
    post = models.Post.get_by_id(id)
    jpost = model_to_dict(post)
    
    return jsonify(
            data = jpost,
            message = "Welcome to this post's show!",
            status = 200
        ), 200



@posts.route('/<id>', methods=['PUT'])
def update_post(id):
    payload = request.get_json()
    print(payload)

    models.Post.update(**payload).where(models.Post.id == id).execute()

    return jsonify(
        data = model_to_dict(models.Post.get_by_id(id)),
        message = f"Congrats, your post is updated successfully! THIS IS YOUR POST==> {model_to_dict(models.Post.get_by_id(id))}",
        status = 200
    ), 200


@posts.route('/<id>', methods=['DELETE'])
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id == id)

    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)

    return jsonify(
        data = {},
        message = f'Successfully deleted {nums_of_rows_deleted} post with id {id}',
        status = 200
    ), 200
