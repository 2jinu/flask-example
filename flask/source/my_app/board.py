from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from my_app import db
from my_app.models.post import Post, WriteForm

PER_PAGE = 10
MAX_PAGE = 10

bp_board = Blueprint(name="board", import_name=__name__, url_prefix="/board/", template_folder="templates/board")

@bp_board.route(rule="/", methods=["GET"])
@login_required
def main():
    page = request.args.get(key="p", default=1, type=int)

    posts = Post.query.order_by(
        Post.created.desc()
    ).paginate(
        page=page,
        per_page=PER_PAGE,
        error_out=False
    )

    if posts.pages <= MAX_PAGE:
        start_page = 1
        end_page = posts.pages
    elif posts.page <= (MAX_PAGE // 2) + 1:
        start_page = 1
        end_page = MAX_PAGE
    elif posts.page >= posts.pages - (MAX_PAGE // 2):
        start_page = posts.pages - (MAX_PAGE - 1)
        end_page = posts.pages
    else:
        start_page = posts.page - (MAX_PAGE // 2)
        end_page = posts.page + (MAX_PAGE // 2)
    
    if end_page == 0:
        end_page = 1

    return render_template(
        template_name_or_list="board.html",
        start_page=start_page,
        end_page=end_page,
        posts=posts
    )

@bp_board.route(rule="/<int:post_id>/", methods=["GET"])
@login_required
def view(post_id:int):
    post = Post.query.get(ident=post_id)
    return render_template(
        template_name_or_list="view.html",
        post=post
    )

@bp_board.route(rule="/write/", methods=["GET", "POST"])
@login_required
def write():
    form = WriteForm()
    if request.method == "GET":
        return render_template("write.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, user=current_user)
            db.session.add(instance=post)
            db.session.commit()
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

    return redirect(location=url_for(endpoint="board.main"))