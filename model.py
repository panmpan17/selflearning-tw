from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    # grade = db.StringProperty(required=True)

    introduction = db.TextProperty(required=True, indexed=False)
    contact = db.ListProperty(str, default=[], indexed=False)
    admin = db.BooleanProperty(default=False)

    @staticmethod
    def toDict(u):
        return {
            "username": u.username,
            "email": u.email,
            "name": u.name,
            "intro": u.introduction,
            "contact": u.contact,
            "admin": u.admin,
            "key": u.key(),
            }

class Activity(db.Model):
    purpose = db.StringProperty(required=True)
    contact = db.ListProperty(str, default=[], indexed=False)
    detail = db.TextProperty(required=True)

    leader = db.StringProperty(required=True)
    team = db.ListProperty(str, default=[])
    approve = db.BooleanProperty(default=False)

    @staticmethod
    def toDict(a):
        return {
            "purpose": a.purpose,
            "contact": a.contact,
            "detail": a.detail,
            "leader": a.leader,
            "team": a.team,
            "approve": a.approve,
            "key": a.key(),
            }

# class Chat(db.Model):
#     team = db.ListProperty(User, default=[])
