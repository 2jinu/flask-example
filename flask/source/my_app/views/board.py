import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user

from my_app import db, app
from my_app.models.user import role_required
from my_app.models.post import Post, File
from my_app.forms.post import WriteForm

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
        template_name_or_list="board/board.html",
        start_page=start_page,
        end_page=end_page,
        posts=posts
    )

@bp_board.route(rule="/write/", methods=["GET", "POST"])
@login_required
@role_required(roles=["ADMIN"])
def write():
    form = WriteForm()
    if request.method == "GET":
        return render_template("board/write.html", form=form)
    
    elif request.method == "POST":
        if form.validate_on_submit():
            files = form.attachments.data
            new_files = []
            if files:
                for file in files:
                    new_file = File(original_name=file.filename)
                    upload_dir = os.path.join(app.static_folder, "upload")

                    if not os.path.exists(path=upload_dir):
                        os.mkdir(path=upload_dir)

                    file.save(os.path.join(upload_dir, new_file.stored_name))
                    new_files.append(new_file)

            new_post = Post(title=form.title.data, content=form.content.data, user=current_user, files=new_files)
            db.session.add(instance=new_post)
            db.session.commit()
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

    return redirect(location=url_for(endpoint="board.main"))

@bp_board.route(rule="/<int:post_id>/", methods=["GET"])
@login_required
def view(post_id:int):
    post = Post.query.get(ident=post_id)
    return render_template(
        template_name_or_list="board/view.html",
        post=post
    )

@bp_board.route(rule="/download/<string:file_id>", methods=["GET"])
@login_required
def download(file_id:int):
    file = File.query.get(ident=file_id)
    if file:
        upload_dir = os.path.join(app.static_folder, "upload")
        file_path = os.path.join(upload_dir, file.stored_name)

        if os.path.exists(path=file_path):
            return send_file(
                path_or_file=file_path,
                as_attachment=True,
                download_name=file.original_name
            )
    
    return redirect(location=url_for(endpoint="board.main"))