from src.model.S3 import s3_connection

from src.config import AWS_S3_BUCKET_NAME

s3 = s3_connection()

def upload(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            AWS_S3_BUCKET_NAME,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

        return f"https://s3.ap-northeast-2.amazonaws.com/gram.stargram/{file.filename}"
    except Exception as e:

        return {"errors": str(e)}
