()
from datetime import date ,datetime , timedelta
from typing import List

from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_avatars import Avatars
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="user")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id") , nullable=True)  # relacja z User
    user: Mapped["User"] = relationship("User", back_populates="posts")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=2))

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # anonimowy user dopuszczony

    post = db.relationship("BlogPost", backref="comments", lazy=True)
    user = db.relationship("User", backref="comments", lazy=True)


with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256' , salt_length=8)
        email = form.email.data
        username = form.username.data

        # Sprawdzenie, czy użytkownik już istnieje
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered, login instead.')
            return redirect(url_for('login'))

        # Tworzenie nowego użytkownika
        new_user = User(
            email=email,
            username=username,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!.')
        login_user(new_user)
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('get_all_posts'))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('get_all_posts'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.username if current_user.is_authenticated else "Anonim",  # zmiana
            user_id=current_user.id if current_user.is_authenticated else None,  # zmiana
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            uid = current_user.id
        else:
            uid = None

        new_comment = Comment(
            text=form.comment.data,
            post_id=post.id,
            user_id=uid
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Komentarz dodany!")
        return redirect(url_for("show_post", post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id)\
                             .order_by(Comment.created_at.desc())\
                             .all()
    return render_template("post.html", post=post, form=form, comments=comments)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user.username if current_user.is_authenticated else post.author  # zmiana
        post.body = edit_form.body.data
        db.session.committ(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/delete-comment/<int:comment_id>")
@admin_only
def delete_comment(comment_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    post_id = comment_to_delete.post_id
    db.session.delete(comment_to_delete)
    db.session.commit()
    flash("Comment deleted successfully!")
    return redirect(url_for('show_post', post_id=post_id))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
