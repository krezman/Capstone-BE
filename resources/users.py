import models

# Dependencies for sending and recieving json data
from flask import Blueprint, request, jsonify

# Dependencies for encrypted login
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user


# User Blueprint
users = Blueprint('users', 'users')

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    print(payload)

    try:
        models.User.get(models.User.email == payload['email'])

        return jsonify(
            data={},
            message="That email has already been used.",
            status= 401
        ), 401
    except models.DoesNotExist:
        hash_pw = generate_password_hash(payload['password'])

        created_user = models.User.create(
            username = payload['username'],
            email = payload['email'],
            password = hash_pw,
            vendor_name = payload['vendor_name'],
            vendor_type = payload['vendor_type'],
            location = payload['location'],
            profile_photo = payload['profile_photo'],
            bio = payload['bio']
        )

        login_user(created_user)

        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)

        return jsonify(
            data = created_user_dict,
            message = f"Successfully registered user with {created_user_dict['email']}",
            status = 201
        ), 201
    


@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    
    try:
        user = models.User.get(models.User.email == payload['email'])

        user_dict = model_to_dict(user)

        check_pw = check_password_hash(user_dict['password'], payload['password'])


        if (check_pw):
            login_user(user)
            loginInfo = user_dict.pop('password')
            # print(user_dict)

            return jsonify(
                data = user_dict,
                message = f"Successfully logged in {user_dict['email']}",
                status =200
            ), 200
        
        else:
            return jsonify(
                data = {},
                message = "Email or password was incorrect.",
                status = 401
            ), 401
    except models.DoesNotExist:
        return jsonify(
            data = {},
            message = "Email or password is incorrect.",
            status = 401
        ), 401
        

@users.route('/logout', methods=["GET"])
def logout():
    logout_user() # this line will need to be imported
    print( "logged out!")
    return jsonify(
        data={},
        status=200,
        message= 'successful logout'
    ), 200

@users.route('/<id>', methods=['GET'])
def profile(id):
    user_profile = models.User.get_by_id(id)
    profile = user_profile.pop('password')
    print(profile)
    return jsonify(
        data = model_to_dict(profile),
        message = f"Successfully retrieved {profile.username}'s page",
        status = 200
    ), 200

@users.route('/index', methods=['GET'])
def profile_index():
    results = models.User.select()
    profile_dicts = [model_to_dict(profile) for profile in results]

    # profiles = profile_dicts.pop('password')

    # for profile_dict in profile_dicts:
    #     profile_dict['post_owner'].pop('password')
    # current_user_post_dicts = [model_to_dict(post) for post in current_user.posts]

    # for post_dict in current_user_post_dicts:
    #     post_dict['post_owner'].pop('password')

    return jsonify({
        'data': profile_dicts,
        'message': "Successfully found profiles!!",
        # 'message': f"Successfully found {len(current_user_post_dicts)} posts.",
        'status': 200
    }), 200
