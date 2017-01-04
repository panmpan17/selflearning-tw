import webapp2
import os
import jinja2

from google.appengine.ext import db
from model import User, Activity# Chat

import hashlib
import re

NAME_PASS_RE = r"[a-zA-Z0-9]{6,16}"
EMAIL_RE = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

def fullmatch(r, text):
    matches = re.findall(r, text)
    if len(matches) == 0:
        return False
    if matches[0] == text:
        return True
    return False

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def setcookie(self,name,value):
        self.response.headers.add_header(
            "Set-Cookie","%s=%s; Path=/" % (name, value)
            )

    def login(self, key):
        self.setcookie("key", str(key))

    def signout(self):
        self.setcookie("key", "")

    def checklogin(self):
        key = self.request.cookies.get("key")
        try:
            u = db.get(key)
            return User.toDict(u)
        except:
            return False

    def needadmin(self):
        u = self.checklogin()

        if not u:
            self.redirect("/")
            return
        # self.write(u)
        if not u["admin"]:
            self.redirect("/")

    @staticmethod
    def hash(text):
        return hashlib.sha256(text).hexdigest()

class Index(Handler):
    def get(self):
        user = self.checklogin()
        if not user:
            self.login("")
        
        actvities_sql = db.GqlQuery(
            "SELECT * FROM Activity WHERE approve=True"
            )

        activities = []
        for a in actvities_sql.run():
            d = Activity.toDict(a)
            u = db.get(d["leader"])
            d["leader"] = User.toDict(u)
            activities.append(d)

        p = {"activities": activities}
        if user:
            p["user"] = user
        self.render("index.html", **p)

class Login(Handler):
    def get(self):
        user = self.checklogin()
        if user:
            self.redirect("/")

        self.render("login.html", err={})

    def post(self):
        user = self.checklogin()
        if user:
            self.redirect("/")

        p = {}
        _type = self.request.get("type")
        if self.request.get("type") == "signup":
            i_username = self.request.get("s_username")
            i_email = self.request.get("s_email")
            i_password = self.request.get("s_password")
            i_name = self.request.get("s_name")
            i_intro = self.request.get("s_intro")
            i_contact = str(self.request.get("s_contact")).split("\n")

            err = {"type": "signup"}

            if not (i_username, i_email, i_password,
                i_name, i_intro, i_contact):
                err["reason"] = "empty"
            elif not (fullmatch(NAME_PASS_RE, i_username)
                and fullmatch(NAME_PASS_RE, i_password)
                and fullmatch(EMAIL_RE, i_email)):
                err["reason"] = "format"
            else:
                u = User(
                    username=i_username,
                    password=Handler.hash(i_password),
                    name=i_name,
                    email=i_email,
                    introduction=i_intro,
                    contact=i_contact
                    )
                u.put()
                self.login(u.key())
                self.redirect("/")
                return
            p["err"] = err
        else:
            i_username = self.request.get("l_username")
            i_password = Handler.hash(self.request.get("l_password"))

            err = {"type": "login"}
            if i_username and i_password:
                user_sql = db.GqlQuery(
                    "SELECT * FROM User WHERE username=:1 AND password=:2",
                    i_username, i_password)
                u = user_sql.fetch(1)
                if len(u) == 1:
                    self.login(user_sql.get().key())
                    self.redirect("/")
                err["reason"] = "password"
            else:
                err["reason"] = "empty"
            p["err"] = err
        self.render("login.html", **p)

class NewActivity(Handler):
    def get(self):
        user = self.checklogin()
        if not user:
            self.redirect("/")

        self.render("newactivity.html")

    def post(self):
        user = self.checklogin()
        if not user:
            self.redirect("/")

        i_purpose = self.request.get("purpose")
        i_contact = self.request.get("contact").split("\n")
        i_detail = self.request.get("detail")

        a = Activity(
            purpose=i_purpose,
            contact=i_contact,
            detail=i_detail,
            leader=str(user["key"]),
            )

        a.put()
        self.redirect("/")

class Admin(Handler):
    def get(self):
        self.needadmin()
        
        actvities_sql = db.GqlQuery(
            "SELECT * FROM Activity WHERE approve=False"
            )

        activities = []
        for a in actvities_sql.run():
            d = Activity.toDict(a)
            u = db.get(d["leader"])
            d["leader"] = User.toDict(u)

            activities.append(d)
        self.render("admin.html", activities=activities)

    def post(self):
        self.needadmin()

        key = self.request.get("key")
        a = db.get(key)
        a.approve = True
        a.put()

        self.redirect("/")
        # self.write(Activity.toDict(a))

class Account(Handler):
    def get(self):
        u = self.checklogin()
        if not u:
            self.redirect("/")

        self.write(u["username"])

app = webapp2.WSGIApplication([
        ("/", Index),
        ("/login", Login),
        ("/newactivity", NewActivity),
        ("/admin", Admin),
        ("/account", Account),
    ], debug=True)
