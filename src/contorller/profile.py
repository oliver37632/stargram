from src.model import session_scope
from src.model.profile import ProfileTbl
from src.model.user import UserTbl
from src.model.feed import FeedTbl
from src.model.photo import PhotoTbl
from src.model.bookmark import BookmarkTbl
from src.contorller.poto import upload
import binascii
from sqlalchemy import or_
def create_profile(name, introduce, link, image, account_id):
    with session_scope() as session:
        user = session.query(UserTbl).filter(UserTbl.account_id == account_id).first()

        if not user:
            return {
                "message": "user is not found"
            }, 404
        new_profile = ProfileTbl(
            id=user.id,
            name=name,
            introduce=introduce,
            link=link,
            photo=upload(image)
        )

        session.add(new_profile)

        session.commit()

        return {
            "message": "success"
        }, 201


def get_profile(account_id):
    with session_scope() as session:

        user = session.query(ProfileTbl).filter(ProfileTbl.account_id == account_id).first()
        if not user:
                return {
                    "message": "NotFound user"
                },404

        return {
            "name": user.name,
            "introduce": user.introduce,
            "link": user.link,
            "image": user.image,
        }, 200


def delete_image(account_id):
    with session_scope() as session:
        user = session.query(ProfileTbl).filter(ProfileTbl.account_id == account_id).first()
        user.image = None

        return {
            "massage": "success"
        }, 204


def modify_profile(name, introduce, link, image, account_id):
    with session_scope() as session:
        user = session.query(ProfileTbl).filter(ProfileTbl.account_id == account_id).first()

        user.image = image
        user.account_id = account_id
        user.link = link
        user.name = name
        user.introduce = introduce

        return {
            "massage": "success"
        }, 204


def search_feed(account_ids):
    with session_scope() as session:

        feed = session.query(FeedTbl.id,
                             FeedTbl.title,
                             FeedTbl.create_at,
                             FeedTbl.heart_count,
                             FeedTbl.comment_count,
                             ProfileTbl.name,
                             PhotoTbl.url,
                             ).filter(UserTbl.account_id == account_ids, UserTbl.id == ProfileTbl.id)\
                             .filter(FeedTbl.user_id == ProfileTbl.id).all()


        return {
                "posts": [{
                    "id_pk": binascii.hexlify(id).decode('utf-8')[:8] + '-' + binascii.hexlify(id).decode('utf-8')[8: 12] + '-' + binascii.hexlify(id).decode('utf-8')[12: 16]+ '-' + binascii.hexlify(id).decode('utf-8')[16: 20] + '-' + binascii.hexlify(id).decode('utf-8')[20:],
                    "title": title,
                    "created_at": str(created_at),
                    "heart_count": heart_count,
                    "comment_count": comment_count,
                    "name": name,
                    "url": url
                       } for id, title, created_at, heart_count, comment_count, name, url in feed]
                   }, 200




def search_like(account_id):
    with session_scope() as session:
        feed = session.query(FeedTbl.id,
                             FeedTbl.title,
                             FeedTbl.create_at,
                             FeedTbl.heart_count,
                             FeedTbl.comment_count,
                             ProfileTbl.name,
                             PhotoTbl.url,
                             ).filter(UserTbl.account_id == account_id, UserTbl.id == ProfileTbl.id)\
                             .filter(FeedTbl.user_id == ProfileTbl.id, FeedTbl.id == BookmarkTbl.feed_id).all()


        return {
                "posts": [{
                    "id_pk": binascii.hexlify(id).decode('utf-8')[:8] + '-' + binascii.hexlify(id).decode('utf-8')[8: 12] + '-' + binascii.hexlify(id).decode('utf-8')[12: 16]+ '-' + binascii.hexlify(id).decode('utf-8')[16: 20] + '-' + binascii.hexlify(id).decode('utf-8')[20:],
                    "title": title,
                    "created_at": str(created_at),
                    "heart_count": heart_count,
                    "comment_count": comment_count,
                    "name": name,
                    "url": url
                       } for id, title, created_at, heart_count, comment_count, name, url in feed]
                   }, 200
