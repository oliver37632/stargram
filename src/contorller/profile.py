from src.model import session_scope
from src.model.profile import ProfileTbl
from src.model.user import UserTbl
from src.model.feed import FeedTbl
from src.model.photo import PhotoTbl
from src.model.heart import HeartTbl
from src.model.bookmark import BookmarkTbl
from src.contorller.poto import upload
import binascii
import pymysql

def create_profile(name, introduce, link, image, account_id):
    with session_scope() as session:
        user = session.query(UserTbl).filter(UserTbl.account_id == account_id).first()
        profile = session.query(ProfileTbl).filter(UserTbl.account_id == account_id, ProfileTbl.id == UserTbl.id).first()
        if not user:
            return {
                "message": "user is not found"
            }, 404

        if profile:
            return {
                "message": "Profile already exists"
            }, 400

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

        user = session.query(ProfileTbl).filter(UserTbl.account_id == account_id, UserTbl.id == ProfileTbl.id).first()
        if not user:
                return {
                    "message": "NotFound user"
                },404

        return {
            "name": user.name,
            "introduce": user.introduce,
            "link": user.link,
            "image": user.photo,
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
        user = session.query(ProfileTbl).filter(UserTbl.account_id == account_id, ProfileTbl.id == UserTbl.id).first()

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

        db = pymysql.connect(
            host='database-1.cj4qlua9nvsk.ap-northeast-2.rds.amazonaws.com',
            port=3306,
            user='admin',
            passwd='oliver37632',
            db='stargram',
            charset='utf8'
        )

        cursor = db.cursor()

        sql = f"select tpro.name, tf.id ,tf.title, tf.create_at, tf.heart_count, tf.comment_count, tp.url, th.id is not NULL as 'heart_exist' from user_tbl tu left join profile_tbl tpro on tu.id = tpro.id left join feed_tbl tf on tu.id = tf.user_id left join photo_tbl tp on tf.id = tp.feed_id left join heart_tbl th on tf.id = th.feed_id where tu.account_id like '{account_ids}'"

        cursor.execute(sql)
        results = cursor.fetchall()

        return {"feeds":[{
            "name": i[0],
            "feed_uuid": binascii.hexlify(i[1]).decode('utf-8')[:8] + '-' + binascii.hexlify(i[1]).decode('utf-8')[8: 12] + '-' + binascii.hexlify(i[1]).decode('utf-8')[12: 16]+ '-' + binascii.hexlify(i[1]).decode('utf-8')[16: 20] + '-' + binascii.hexlify(i[1]).decode('utf-8')[20:],
            "title": i[2],
            "create_at": str(i[3]),
            "heart_count": i[4],
            "comment_count": i[5],
            "image": i[6],
            "heart_status": bool(i[7]),
        } for i in results]},200





def search_like(account_id):
    with session_scope() as session:
        db = pymysql.connect(
            host='database-1.cj4qlua9nvsk.ap-northeast-2.rds.amazonaws.com',
            port=3306,
            user='admin',
            passwd='oliver37632',
            db='stargram',
            charset='utf8'
        )

        cursor = db.cursor()

        sql = f"select tpro.name, tf.id ,tf.title, tf.create_at, tf.heart_count, tf.comment_count, tp.url, bt.id, th.id is not NULL as 'heart_exist' from user_tbl tu left join profile_tbl tpro on tu.id = tpro.id left join feed_tbl tf on tu.id = tf.user_id left join photo_tbl tp on tf.id = tp.feed_id left join heart_tbl th on tf.id = th.feed_id left join bookmark_tbl bt on tf.id = bt.feed_id where tu.account_id like '{account_id}' AND bt.id is not null;"

        cursor.execute(sql)
        results = cursor.fetchall()

        return {"feeds": [{
            "name": i[0],
            "feed_uuid": binascii.hexlify(i[1]).decode('utf-8')[:8] + '-' + binascii.hexlify(i[1]).decode('utf-8')[8: 12] + '-' + binascii.hexlify(i[1]).decode('utf-8')[12: 16] + '-' + binascii.hexlify(i[1]).decode('utf-8')[16: 20] + '-' + binascii.hexlify(i[1]).decode('utf-8')[20:],
            "title": i[2],
            "create_at": str(i[3]),
            "heart_count": i[4],
            "comment_count": i[5],
            "image": i[6],
            "heart_status": bool(i[7]),
        } for i in results]}, 200


def search(keyword):
    with session_scope() as session:
        feed = session.query(FeedTbl.id,
                             FeedTbl.title,
                             FeedTbl.create_at,
                             FeedTbl.heart_count,
                             FeedTbl.comment_count,
                             PhotoTbl.url).filter(FeedTbl.title.ilike(f'%{keyword}%'), FeedTbl.id == PhotoTbl.feed_id)
        return {
                "posts": [{
                    "id_pk": binascii.hexlify(id).decode('utf-8')[:8] + '-' + binascii.hexlify(id).decode('utf-8')[8: 12] + '-' + binascii.hexlify(id).decode('utf-8')[12: 16]+ '-' + binascii.hexlify(id).decode('utf-8')[16: 20] + '-' + binascii.hexlify(id).decode('utf-8')[20:],
                    "title": title,
                    "created_at": str(created_at),
                    "heart_count": heart_count,
                    "comment_count": comment_count,
                    "url": url
                       } for id, title, created_at, heart_count, comment_count, url in feed]
                   }, 200

