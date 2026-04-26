from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Results, Questions
from conf import db

class SubmitResultAPI(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"status": "error", "message": "User not found"}, 404

        data = request.get_json()
        total_questions = data.get("totalQuestions", 0)
        answered_questions = data.get("answeredQuestions", 0)
        correct_answers = data.get("correctAnswers", 0)
        num_questions_selected = data.get("numQuestionsSelected", 10)
        answers = data.get("answers", [])

        try:
            result = Results(
                user_id=user.id,
                total_ques_count=total_questions,
                answered_ques_count=answered_questions,
                correct_ans_count=correct_answers,
                num_questions_selected=num_questions_selected
            )
            db.session.add(result)
            db.session.commit()

            questions_to_add = []
            for ans_data in answers:
                question = Questions(
                    result_id=result.id,
                    question=ans_data.get("question"),
                    correct_ans=ans_data.get("correctAnswer"),
                    user_selected_ans=ans_data.get("userAnswer"),
                    is_correct=ans_data.get("isCorrect")
                )
                questions_to_add.append(question)
                
            db.session.add_all(questions_to_add)
            db.session.commit()

            return {
                "status": "success",
                "message": "Result saved successfully",
                "result_id": result.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"status": "exception", "message": str(e)}, 500
