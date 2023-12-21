from datetime import timedelta
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from my_app import db, rc, logger
from my_app.forms.user import LoginForm, RegistrationForm
from my_app.models.user import User
from my_app.models.role import Role

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
            login_attempts = rc.get(name=form.username.data)
            if login_attempts:
                try:
                    login_attempts = int(login_attempts.decode())
                    if login_attempts >= 5:
                        locked_time = rc.ttl(name=form.username.data)
                        minute, seccond = divmod(locked_time, 60)
                        flash(message=f"{minute:02d}:{seccond:02d} 뒤에 시도하세요.")
                        return redirect(location=url_for(endpoint="index.login"))
                except ValueError:
                    login_attempts = None

            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(password=form.password.data):
                    rc.delete(user.username)
                    login_user(user=user)
                    session.permanent = True
                    session.modified = True
                    logger.info(
                        msg=f"Login Success : {user.username}",
                        extra={
                            "remote_addr": request.remote_addr,
                            "method": request.method,
                            "url": request.path,
                            "version": request.environ.get('SERVER_PROTOCOL')
                        }
                    )
                    return redirect(location=url_for(endpoint="board.main"))
                else:
                    if login_attempts:
                        rc.incr(name=user.username)
                    else:
                        rc.set(name=user.username, value=1, ex=timedelta(minutes=5))
                
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
            role = Role.query.filter_by(name="USER").first()
            if not role:
                flash(message="권한 오류가 발생하였습니다.")
                return redirect(location=url_for(endpoint="index.login"))

            user = User(
                username=form.username.data,
                password=form.password.data,
                roles=[role]
            )
            db.session.add(instance=user)
            try:
                db.session.commit()
                login_user(user=user)
                return redirect(location=url_for(endpoint="board.main"))
            
            except IntegrityError as e:
                db.session.rollback()
                if e.orig.args and e.orig.args[0] == 1062:
                    flash(message="중복된 사용자입니다.")
                else:
                    flash(message="알 수 없는 오류입니다.")
        else:
            for _, values in form.errors.items():
                for value in values:
                    flash(message=value)

        return redirect(location=url_for(endpoint="index.login"))
  
@bp_index.route(rule="/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(location=url_for(endpoint="index.login"))
