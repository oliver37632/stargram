from functools import wraps
from flask import request, abort


def validate_JSON(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                instance = model(getattr(request, 'json'))
                instance.validate()
            except:
                abort(400, "check JSON")

            return func(*args, **kwargs)
        return wrapper
    return decorator