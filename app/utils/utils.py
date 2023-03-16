import re
import random
import string
from ..db_class.db import User

def isUUID(uuid):
    return re.match(r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$", uuid)


def generate_api_key(length=60):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))



def get_user_api(api_key):
    return User.query.filter_by(api_key=api_key).first()


def verif_api_key(headers):
    if not "X-API-KEY" in headers:
        return {"message": "Error no API key pass"}, 403
    user = get_user_api(headers["X-API-KEY"])
    if not user:
        return {"message": "API key not found"}, 403
    return {}