from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.contorller.auth import signup, login, id_overlap_check, refresh_token, email_send, check_code


class SignUp(Resource):
    def post(self):
        account_id = request.json['account_id']
        email = request.json['email']
        password = request.json['password']

        return signup(
                account_id=account_id,
                email=email,
                password=password
                     )


class Login(Resource):
    def post(self):
        account_id = request.json['account_id']
        password = request.json['password']

        return login(
            account_id=account_id,
            password=password
        )


class Id_Check(Resource):
    def post(self):
        account_id = request.json['account_id']

        return id_overlap_check(
            account_id=account_id
        )


class Token_Refresh(Resource):
    @jwt_required(refresh=True)
    def put(self):
        token = get_jwt_identity()

        return refresh_token(token)


class Email_Send(Resource):
    def post(self):
        email = request.json['email']

        return email_send(email)


class CheckEmailCode(Resource):
    def post(self):
        email = request.json['email']
        code = request.json['code']

        return check_code(email=email,
                          code=code)


