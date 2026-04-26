from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User
from conf import ag_ph
from argon2.exceptions import VerifyMismatchError

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"status": "error", "message": "Username and password are required"}, 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"status": "error", "message": "Invalid username or password"}, 401

        try:
            ag_ph.verify(hash=user.password, password=password)
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return {
                "status": "success",
                "message": "Login successful",
                "access": access_token,
                "refresh": refresh_token,
                "user": {"id": user.id, "username": user.username}
            }, 200

        except VerifyMismatchError:
            return {"status": "error", "message": "Invalid username or password"}, 401
        except Exception as e:
            return {"status": "exception", "message": str(e)}, 500
