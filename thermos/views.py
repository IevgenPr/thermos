from flask import render_template, url_for, request, redirect, flash, abort

from thermos import app, db, login_manager
from .forms import BookmarkForm, LoginForm, SignUpForm
from .models import User, Bookmark, Tag
from flask_login import login_required, login_user, logout_user, current_user


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


@app.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@app.route("/add", methods=["GET", "POST"])  # to respond to both get and post
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        # print("Form errors: {}".format(form.url.errors))
        description = form.description.data
        # store_bookmark(url)
        tags = form.tags.data
        bm = Bookmark(user=current_user, url=url, description=description, tags=tags)
        db.session.add(bm)
        db.session.commit()
        flash("stored url: {}".format(url))
        return redirect(url_for('index'))
    # if request.method == "POST":
    #     url = request.form['url']
    #     store_bookmark(url)
    #     flash("stored url: {}".format(url))
    #
    #     return redirect(url_for('index'))
    return render_template("bookmark_form.html", form=form, title="Add Bookmark")


@app.route("/delete/<int:bookmark_id>", methods=["GET", "POST"])  # to respond to both get and post
@login_required
def delete(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash("deleted: {}".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    else:
        flash("Please confirm deleting the bookmark")
    return render_template("confirm_delete.html", bookmark=bookmark, nolinks=True)


@app.route("/edit/<int:bookmark_id>", methods=["GET", "POST"])  # to respond to both get and post
@login_required
def edit(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    print(bookmark, bookmark.tags)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        url = form.url.data
        db.session.commit()
        flash("stored: {}".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template("bookmark_form.html", form=form, title="Edit bookmark")


@app.route("/login", methods=["GET", "POST"])  # to respond to both get and post
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user',
                                                                username=user.username))
        flash("Incorrect username or password.")
    return render_template("login.html", form=form)

@app.route("/signup", methods=["GET", "POST"])  # to respond to both get and post
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Welcome, {}! Please login.".format(user.username))
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/tag/<name>")
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

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
