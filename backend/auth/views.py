from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from ..user_schema import UserCreateSchema, UserSchema
from ..extensions import db, pwd_context, jwt
from ..models import User
from marshmallow import ValidationError
from .helpers import add_token_to_database, revoke_token, is_token_revoked

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400
    keycode = request.json.get("keycode")
    if keycode != current_app.config["REGISTRATION_KEY"]:
        return {"msg": "Invalid registration key"}, 403

    schema = UserCreateSchema()
    user = schema.load(request.json)
    db.session.add(user)
    db.session.commit()

    schema = UserSchema()

    return {"msg": "User created", "user": schema.dump(user)}


@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return {"msg": "Missing username or password"}, 400

    user = User.query.filter_by(username=username).first()
    if not user or not pwd_context.verify(password, user.password):
        return {"msg": "Bad Credentials"}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token)
    add_token_to_database(refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    add_token_to_database(access_token)
    return {"access_token": access_token}, 200


@auth_blueprint.route("revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return {"msg": "Token revoked"}, 200


@auth_blueprint.route("revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return {"msg": "Refresh token revoked"}, 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    try:
        return is_token_revoked(jwt_payload)
    except Exception:
        return True


@jwt.user_lookup_loader
def load_user(jwt_headers, jwt_payload):
    identity_claim = current_app.config["JWT_IDENTITY_CLAIM"]
    user_id = jwt_payload[identity_claim]
    return User.query.get(user_id)


@auth_blueprint.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return UserSchema().dump(user), 200


@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return {"msg": "Logged out successfully"}, 200


@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
