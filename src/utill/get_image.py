from src.model import session_scope
from src.model.photo import PhotoTbl
from src.model.feed import FeedTbl

def get_url(feed_id: str):
    with session_scope() as session:
        url = session.query(PhotoTbl.url).filter(PhotoTbl.feed_id == feed_id).all()
        print("url : ",url)
        return str(url)