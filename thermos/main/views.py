from flask import render_template, url_for, request, redirect, flash, abort

from thermos import app, db, login_manager
from .models import User, Bookmark, Tag


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


# def logged_in_user():
#     return User.query.filter_by(username='ipr').first()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
                           title="zzzzzz",
                           user= "ipr", # "#models.User("ie", "pr"),
                           text=["one", "two", "three"],
                           new_bookmarks=Bookmark.newest(5))  # new_bookmarks(5))


@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.context_processor  # make globally available in template context
def inject_tags():
    return dict(all_tags=Tag.all)
