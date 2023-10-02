"""Blogly application."""

from flask import Flask, redirect, request, render_template, session
from models import db, connect_db, User, Post, Tag
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'seecreeett'

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """List the users"""
    redirect("/users")

@app.route('/users')
def list_users():
    """Show the list of users"""
    users = User.query.all()
    return render_template("index.html",userlist=users)

@app.route("/users/new")
def show_add_user():
    """Add a new user"""
    render_template("add_user.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Handle the adding of new user"""
    added_user = User(first_name=request.form['first_name'], last_name=request.form["last_name"], image_url=request.form['image_url'] or None)
    db.session.add(added_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show a specific user."""
    user = User.query.get_or_404(user_id)
    return render_template("show_user.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show the edit user screen"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def submit_edit(user_id):
    """Submit the edit user"""
    user=User.query.get_or_404(user_id)
    user.first_name= request.form['first_name']
    user.last_name= request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_destroy(user_id):
    """Handle user deletion"""
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """show the create post screen."""
    user = User.query.get_or_404(user_id)
    tags= Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post_new(user_id):
    """add new post"""
    user= User.query.get_or_404(user_id)
    tag_ids = []
    for num in request.form.getlist("tags"):
        tag_ids.append(num)
    tags = User.query.filter(Tag.id.in_(tag_ids)).all()
    post= Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Show post details"""
    post=Post.query.get_or_404(post_id)
    
    return render_template("show_post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """edit post form"""
    tags = Tag.query.all()
    tag_ids = []
    for num in request.form.getlist("tags"):
        tag_ids.append(num)
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """edit post"""
    post= Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
  
    tag_ids = []
    for num in request.form.getlist("tags"):
        tag_ids.append(num)
    tags = User.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods= ["POST"])
def delete_post(post_id):
    """delete post"""
    post= Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def tags_list():
    """ Show page with tags"""
    tags = Tag.query.all()
    return render_template("list_tags.html", tags= tags)

@app.route("/tags/new")
def new_tag_form():
    """show add new tag form"""
    return render_template("new_tag.html")

@app.route("/tags/new", methods=["POST"])
def new_tag():
    """add a new tag"""
    new_tag = Tag(name= request.form["name"])
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def tag_info(tag_id):
    """show a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("show_tag.html", tag=tag)

@app.route("/tags/edit/<int:tag_id>")
def tag_edit_show(tag_id):
    """show edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/edit/<int:tag_id>", methods=["POST"])
def tag_edit(tag_id):
    """edit a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit(tag)
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods={"POST"})
def tag_delete(tag_id):
    """delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")