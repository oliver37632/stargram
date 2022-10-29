from src.model import session_scope, Redis
from flask import abort
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from src.model.user import UserTbl
from src.contorller.email import send_email
import bcrypt

import random

import uuid


def signup(account_id, email, password):
    with session_scope() as session:
        user = session.query(UserTbl.account_id, UserTbl.password).filter(UserTbl.account_id == account_id).first()

        if not user:
            new_sigup = UserTbl(
                id=uuid.uuid1().bytes_le,
                account_id=account_id,
                email=email,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            )

            session.add(new_sigup)
            session.commit()

            return {
                       "message": "success"
                   }, 201
        return {
            "message": "overlap"
        }, 403


def login(account_id, password):
    with session_scope() as session:
        user = session.query(UserTbl).filter(UserTbl.account_id == account_id)
        if not user.scalar():
            abort(409, 'user id code does not match')

        user = user.first()

        check_user_pw = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

        if not check_user_pw:
            abort(409, 'user password code does not match')

        access_expires_delta = timedelta(minutes=60)
        refresh_expires_delta = timedelta(weeks=1)

        access_token = create_access_token(expires_delta=access_expires_delta,
                                           identity=account_id
                                           )
        refresh_token = create_refresh_token(expires_delta=refresh_expires_delta,
                                             identity=account_id
                                             )

        Redis.setex(name=account_id,
                    value=refresh_token,
                    time=refresh_expires_delta)

        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 201


def id_overlap_check(account_id):
    with session_scope() as session:
        user = session.query(UserTbl.account_id).filter(UserTbl.account_id == account_id)

        if user.scalar():
            return {
                "message": "nick overlap"
            }, 409
        return {
            "message": "Available"
        }, 200


def refresh_token(token):
    with session_scope() as session:

        user = session.query(UserTbl).filter(UserTbl.account_id == token).first()
        if not user:
            Redis.delete(token)
            return {
                "message": "user is not found"
            }, 404
        tokens = Redis.get(token)
        access_expires_delta = timedelta(minutes=60)
        refresh_expires_delta = timedelta(weeks=1)

        if tokens:
            Redis.delete(token)

            refresh_token = create_refresh_token(expires_delta=refresh_expires_delta,
                                                 identity=token
                                                 )

            access_token = create_access_token(expires_delta=access_expires_delta,
                                               identity=token
                                               )

            Redis.setex(name=token,
                        value=refresh_token,
                        time=refresh_expires_delta)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            },201


def email_send(email):
    with session_scope() as session:
        user = session.query(UserTbl.email).filter(UserTbl.email == email).scalar()

        if user:
            abort(409, 'this email is already in use')

        code = f"{random.randint(111111, 999999):04d}"
        title = "STARGRMA 이메일 인증 메일"
        content = f"이메일 인증 코드는 {code}입니다."

        send_email(title=title,
                   content=content,
                   adress=email)

        Redis.setex(name=email,
                    value=code,
                    time=180)

        return {
                   "message": "success"
               }, 200

def check_code(email, code):
    stored_code = Redis.get(email)

    if not stored_code:
        abort(404, 'this email does not exist')

    if int(stored_code) != int(code):
        abort(409, 'email and code does not match')

    return {
        "message": "success"
    }, 200
