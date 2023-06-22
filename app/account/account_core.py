from .. import db
from ..db_class.db import User, Role, Org, Case_Org, Task_User
import bleach

def get_all_roles():
    """Return all roles"""
    return Role.query.all()

def get_all_orgs():
    """Return all organisations"""
    return Org.query.all()

def get_user(id):
    """Return the user"""
    return User.query.get(id)

def get_org(id):
    """Return the org"""
    return Org.query.get(id)



def edit_user_core(form_dict, id):
    """Edit the user to the DB"""
    user = get_user(id)

    user.first_name=bleach.clean(form_dict["first_name"])
    user.last_name=bleach.clean(form_dict["last_name"])
    user.email=bleach.clean(form_dict["email"])

    db.session.commit()