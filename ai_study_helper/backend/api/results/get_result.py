from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Results, Questions
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

class QuestionSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Questions
        load_instance = True
        exclude = ("result_id",)

class ResultSerializer(SQLAlchemyAutoSchema):
    questions = fields.Nested(QuestionSerializer, many=True)
    class Meta:
        model = Results
        load_instance = True
        include_relationships = True

result_schema = ResultSerializer()
results_schema = ResultSerializer(many=True)

class GetAllResultAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        results = Results.query.filter_by(user_id=user_id).order_by(Results.id.desc()).all()
        return {
            "status": "success",
            "results": results_schema.dump(results)
        }, 200

class GetOneResultAPI(Resource):
    @jwt_required()
    def get(self, result_id):
        user_id = get_jwt_identity()
        result = Results.query.filter_by(id=result_id, user_id=user_id).first()
        
        if not result:
            return {"status": "error", "message": "Result not found"}, 404
            
        return {
            "status": "success",
            "result": result_schema.dump(result)
        }, 200
