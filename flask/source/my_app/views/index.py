from sqlalchemy.exc import IntegrityError
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user

from my_app import db
from my_app.forms.user import LoginForm, RegistrationForm
from my_app.models.user import User, Role

bp_index = Blueprint(
    name="index",
    import_name=__name__,
    url_prefix="/"
)

@bp_index.route(rule="/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(location=url_for(endpoint="board.main"))
    
    form=LoginForm()
    
    if request.method == "GET":
        return render_template(
            template_name_or_list="user/login.html",
            form=form
        )
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(password=form.password.data):
                    login_user(user=user)
                    return redirect(location=url_for(endpoint="board.main"))
                
            flash(message="로그인에 실패하였습니다.")
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

        return redirect(location=url_for(endpoint="index.login"))

@bp_index.route(rule="/regist", methods=["GET", "POST"])
def regist():
    if current_user.is_authenticated:
        return redirect(location=url_for(endpoint="board.main"))
    
    form = RegistrationForm()
    
    if request.method == "GET":
        return render_template(
            template_name_or_list="user/regist.html",
            form=form
        )
    else:
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data, roles=[Role.query.filter_by(name="USER").first()])
            db.session.add(instance=user)
            try:
                db.session.commit()
                login_user(user=user)
                return redirect(location=url_for(endpoint="board.main"))
            
            except IntegrityError as e:
                db.session.rollback()
                if e.orig.args and e.orig.args[0] == 1062:
                    flash("중복된 사용자입니다.")
                else:
                    flash("알 수 없는 오류입니다.")
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

        return redirect(location=url_for(endpoint="index.login"))
  
@bp_index.route(rule="/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(location=url_for(endpoint="index.login"))
