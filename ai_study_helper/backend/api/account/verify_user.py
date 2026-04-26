from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

class UserVerifyAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return {"status": "error", "message": "User not found"}, 404
            
        return {
            "status": "success",
            "message": f"Hey {user.username}!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.strftime("%B %d, %Y")
            }
        }, 200
