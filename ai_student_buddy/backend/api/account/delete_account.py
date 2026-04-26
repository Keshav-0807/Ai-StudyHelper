from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from conf import db, ag_ph
from argon2.exceptions import VerifyMismatchError

class DeleteAccountAPI(Resource):

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        # Require password confirmation — never delete without verifying identity
        password = data.get("password")
        if not password:
            return {
                "status": "error",
                "message": "Password is required to delete your account",
            }, 400

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {
                "status": "error",
                "message": "User not found",
            }, 404

        # Verify the password before deletion
        try:
            ag_ph.verify(hash=user.password, password=password)
        except VerifyMismatchError:
            return {
                "status": "error",
                "message": "Incorrect password. Account not deleted.",
            }, 401

        # Delete user — cascade will automatically delete all Results and Questions
        db.session.delete(user)
        db.session.commit()

        return {
            "status": "success",
            "message": "Your account and all associated data have been permanently deleted.",
        }, 200
