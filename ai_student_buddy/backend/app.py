from conf import api, app, db
from api import (
    RegistrationAPI, LoginAPI, UserVerifyAPI,
    GenerateQuizAPI, SubmitResultAPI,
    RefreshTokenAPI, GetOneResultAPI, GetAllResultAPI,
    DeleteAccountAPI,
)
import os

# Account routes
api.add_resource(RegistrationAPI,  "/register")
api.add_resource(LoginAPI,         "/login")
api.add_resource(UserVerifyAPI,    "/verify")
api.add_resource(RefreshTokenAPI,  "/refresh")
api.add_resource(DeleteAccountAPI, "/account")

# Quiz route
api.add_resource(GenerateQuizAPI,  "/upload")

# Results routes
api.add_resource(SubmitResultAPI,  "/submit-result")
api.add_resource(GetAllResultAPI,  "/results-data")
api.add_resource(GetOneResultAPI,  "/results-data/<int:result_id>")

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)
