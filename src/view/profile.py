from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.contorller.profile import create_profile, get_profile, delete_image, modify_profile, search_feed, search_like


class Create_Profile(Resource):
    @jwt_required()
    def post(self):
        account_id = get_jwt_identity()
        name = request.form['name']
        introduce = request.form['introduce']
        link = request.form['link']
        image = request.files.getlist("image")

        return create_profile(name, introduce, link, image, account_id)

    @jwt_required()
    def get(self):
        account_id = get_jwt_identity()
        return get_profile(account_id)

    @jwt_required()
    def delete(self):
        account_id = get_jwt_identity()
        return delete_image(account_id)

    @jwt_required()
    def patch(self):
        account_id = get_jwt_identity()
        name = request.form['name']
        introduce = request.form['introduce']
        link = request.form['link']
        image = request.files.getlist("image")
        return modify_profile(name, introduce, link, image, account_id)


class Search_Feed(Resource):
    @jwt_required()
    def get(self):
        account_id = get_jwt_identity()
        return search_feed(account_id)

class Search_Book(Resource):
    @jwt_required()
    def get(sel):
        account_id = get_jwt_identity()
        return search_like(account_id)