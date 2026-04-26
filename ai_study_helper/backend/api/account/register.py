from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User
from conf import db, ag_ph
from sqlalchemy.exc import IntegrityError

class RegistrationAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password:
            return {"status": "error", "message": "Username and password are required"}, 400

        try:
            hashed_password = ag_ph.hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=str(new_user.id))
            refresh_token = create_refresh_token(identity=str(new_user.id))

            return {
                "status": "success",
                "message": "User created successfully",
                "access": access_token,
                "refresh": refresh_token,
                "user": {"id": new_user.id, "username": new_user.username}
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"status": "error", "message": "Username already exists"}, 400
        except Exception as e:
            db.session.rollback()
            return {"status": "exception", "message": str(e)}, 500
