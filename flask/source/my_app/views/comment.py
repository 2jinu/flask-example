from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user

from my_app import db, app
from my_app.models.post import Post
from my_app.models.comment import Comment
from my_app.forms.comment import CommentForm

bp_comment = Blueprint(name="comment", import_name=__name__, url_prefix="/board/<int:post_id>/comment/", template_folder="templates/board")

@bp_comment.route(rule="/write/", methods=["POST"])
@login_required
def write(post_id:int):
    post = Post.query.get(ident=post_id)
    if not post:
        flash("존재하지 않는 게시물입니다.")
        return redirect(location=url_for(endpoint="board.main"))
    
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, secret=form.secret.data, username=current_user.username)
        post.comments.append(new_comment)
        current_user.comments.append(new_comment)
        db.session.add(instance=new_comment)
        db.session.commit()
    else:
        for _, values in form.errors.items():
            for value in values:
                flash(message=value)

    return redirect(location=url_for(endpoint="board.view", post_id=post_id))

@bp_comment.route(rule="<int:comment_id>/delete/", methods=["GET"])
@login_required
def delete(comment_id:int, post_id:int):
    if current_user.is_admin():
        comment = Comment.query.filter_by(id=comment_id).first()
    else:
        comment = Comment.query.filter_by(id=comment_id, username=current_user.username).first()
    
    if comment:
        db.session.delete(instance=comment)
        db.session.commit()
    
    return redirect(location=url_for(endpoint="board.view", post_id=post_id))