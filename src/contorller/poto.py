import random

from src.model.S3 import s3_connection, s3_put_object

from src.config import AWS_S3_BUCKET_NAME

s3 = s3_connection()

def upload(image):
    for f in image:
        name = random.randint(0, 9999)
        f.save("./temp")
        s3_put_object(s3, AWS_S3_BUCKET_NAME, "./temp", name)
        location = s3.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME)['LocationConstraint']
        image_url = f'https://{AWS_S3_BUCKET_NAME}.s3.{location}.amazonaws.com/{name}'


        return image_url


