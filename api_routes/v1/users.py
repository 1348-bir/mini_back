from flask import jsonify, request, abort
from . import api_v1
from .models import User, db  # 确保正确导入 User 模型和 db

@api_v1.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return jsonify({"message": "Get all users", "users": [{"id": user.id, "userid": user.userid, "realname": user.realname} for user in users]})

@api_v1.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify({"message": f"Get user {user_id}", "user": {"id": user.id, "userid": user.userid, "realname": user.realname}})
    else:
        abort(404, description="User not found")

@api_v1.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Create user", "data": data}), 201

@api_v1.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": f"Update user {user_id}", "data": data})
    else:
        abort(404, description="User not found")

@api_v1.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Delete user {user_id}"}), 204
    else:
        abort(404, description="User not found")
