from flask import Blueprint
from flask_restful import Api

bp = Blueprint("gramo", __name__, url_prefix="")
api_basic = Api(bp)

from src.view.auth import SignUp
api_basic.add_resource(SignUp, "/auths")

from src.view.auth import Email_Send
api_basic.add_resource(Email_Send, "/auths/email")

from src.view.auth import CheckEmailCode
api_basic.add_resource(CheckEmailCode, "/auths/email/check")

from src.view.auth import Login
api_basic.add_resource(Login, "/auths/login")

from src.view.auth import Token_Refresh
api_basic.add_resource(Token_Refresh, "/auths")

from src.view.auth import Id_Check
api_basic.add_resource(Id_Check, "/auths/id/check")

from src.view.profile import Create_Profile
api_basic.add_resource(Create_Profile, "/profiles")

from src.view.profile import Search_Feed
api_basic.add_resource(Search_Feed, "/profiles/feed")

from src.view.profile import Search_Book
api_basic.add_resource(Search_Book, "/profiles/favorites")