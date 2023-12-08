import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file, session
from flask_login import login_required, current_user

from my_app import db, app
from my_app.models.post import Post, File
from my_app.forms.post import WriteForm, CommentForm

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
def write():
    form = WriteForm()
    if request.method == "GET":
        return render_template("board/write.html", form=form)
    
    elif request.method == "POST":
        if form.validate_on_submit():
            files = form.attachments.data
            new_files = []
            if files:
                upload_dir = os.path.join(app.static_folder, "upload")
                if not os.path.exists(path=upload_dir):
                    os.mkdir(path=upload_dir)

                for file in files:
                    new_file = File(file=file)
                    file.save(os.path.join(upload_dir, new_file.stored_name))
                    new_files.append(new_file)

            new_post = Post(title=form.title.data, content=form.content.data, user=current_user, files=new_files)
            db.session.add(instance=new_post)
            db.session.commit()
            return redirect(location=url_for(endpoint="board.view", post_id=new_post.id))
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

    return redirect(location=url_for(endpoint="board.main"))

@bp_board.route(rule="/<int:post_id>/", methods=["GET"])
@login_required
def view(post_id:int):
    post = Post.query.get(ident=post_id)
    if not post:
        flash(message="존재하지 않는 게시물입니다.")
        return redirect(location=url_for(endpoint="board.main"))
    
    if "views" not in session:
        session["views"] = []
    
    if post_id not in session["views"]:
        session["views"].append(post_id)
        post.views += 1
        db.session.commit()

    form = CommentForm()
    post.comments = list(reversed(post.comments))
    return render_template(
        template_name_or_list="board/view.html",
        post=post,
        form=form
    )

@bp_board.route(rule="/<int:post_id>/delete", methods=["GET"])
@login_required
def delete(post_id:int):
    if current_user.is_admin():
        post = Post.query.filter_by(id=post_id).first()
    else:
        post = Post.query.filter_by(id=post_id, user=current_user).first()
    
    if post:
        if post.files:
            upload_dir = os.path.join(app.static_folder, "upload")
            for file in post.files:
                file_path = os.path.join(upload_dir, file.stored_name)
                if os.path.exists(file_path):
                    os.remove(file_path)

                db.session.delete(instance=file)

        db.session.delete(instance=post)
        db.session.commit()
    
    return redirect(location=url_for(endpoint="board.main"))

@bp_board.route(rule="/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id:int):
    post = Post.query.filter_by(id=post_id, user=current_user).first()
    if post:
        form = WriteForm()
        if request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
            return render_template("board/edit.html", form=form, post_id=post_id)
        elif request.method == "POST":
            if form.validate_on_submit():
                upload_dir = os.path.join(app.static_folder, "upload")

                for file in post.files:
                    file_path = os.path.join(upload_dir, file.stored_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    db.session.delete(instance=file)
                
                post.title = form.title.data
                post.content = form.content.data

                files = form.attachments.data
                if files:
                    new_files = []
                    for file in files:
                        new_file = File(file=file)
                        file.save(os.path.join(upload_dir, new_file.stored_name))
                        new_files.append(new_file)

                    post.files = new_files
                db.session.commit()

                return redirect(location=url_for(endpoint="board.view", post_id=post.id))
            else:
                for _, values in form.errors.items():
                    for value in values:
                        flash(message=value)
    else:
        flash(message="존재하지 않는 게시물입니다.")
    
    return redirect(location=url_for(endpoint="board.main"))

@bp_board.route(rule="/<int:post_id>/files/<string:file_id>", methods=["GET"])
@login_required
def download(post_id:int, file_id:int):
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
    
    return redirect(location=url_for(endpoint="board.view", post_id=post_id))