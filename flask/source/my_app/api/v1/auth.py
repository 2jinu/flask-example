from flask import make_response, jsonify
from flask_restx import Namespace, Resource, reqparse, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from my_app import rc
from my_app.models.user import User

auth_namespace = Namespace(name="auth", description="Authentication API")
resource_parser = reqparse.RequestParser()
refresh_parser = reqparse.RequestParser()
resource_parser.add_argument("Authorization", help="Bearer {access_token}", type=str, required=True, location="headers", default="Bearer ")
refresh_parser.add_argument("Authorization", help="Bearer {refresh_token}", type=str, required=True, location="headers", default="Bearer ")

token_req_model = auth_namespace.model(name="토큰 발급 요청 모델", model={
    "username": fields.String(required=True, description="사용자 아이디"),
    "password": fields.String(required=True, description="사용자 비밀번호")
})
token_res_model = auth_namespace.model(name="토큰 발급 응답 모델", model={
    "access_token": fields.String(description="액세스 토큰"),
    "refresh_token" : fields.String(description="재발급 토큰")
})
token_patch_model = auth_namespace.model(name="토큰 갱신 응답 모델", model={
    "access_token": fields.String(description="액세스 토큰")
})
user_model = auth_namespace.model(name="사용자 모델", model={
    "id": fields.String(description="사용자 식별 값"),
    "username": fields.String(description="사용자 아이디"),
    "roles": fields.List(description="사용자 역할", cls_or_instance=fields.String())
})

@auth_namespace.route("/tokens")
class Token(Resource):
    @auth_namespace.doc(description="""JWT 토큰을 발급하는 API입니다.""")
    @auth_namespace.expect(token_req_model)
    @auth_namespace.marshal_with(fields=token_res_model, code=201, description="토큰 발급 성공")
    def post(self):
        """토큰 발급"""

        args    = auth_namespace.payload
        user    = User.query.filter_by(username=args.get("username")).first()

        if user and user.check_password(password=args.get("password")):
            access_token    = create_access_token(identity=user.id)
            refresh_token   = create_refresh_token(identity=user.id)
            return dict(access_token=access_token, refresh_token=refresh_token), 201

        return make_response(jsonify(msg="Unauthorized"), 401)
    
    @auth_namespace.doc(description="""인증 토큰을 갱신하는 API입니다.""")
    @auth_namespace.expect(refresh_parser)
    @auth_namespace.marshal_with(fields=token_patch_model, code=201)
    @jwt_required(refresh=True)
    def patch(self):
        """토큰 갱신"""
        
        access_token = create_access_token(identity=get_jwt_identity())
        return dict(access_token=access_token), 201
    
    @auth_namespace.doc(description="""인증 토큰을 폐기하는 API입니다.\n로그 아웃과 같은 기능으로 인증 토큰을 폐기하고 재사용을 방지합니다.""")
    @auth_namespace.expect(resource_parser)
    @auth_namespace.response(code=204, description="토큰이 성공적으로 폐기되었을 때 반환")
    @jwt_required()
    def delete(self):
        """토큰 폐기"""

        rc.set(name=get_jwt().get("jti"), value="")
        return "", 204
        
@auth_namespace.route("/users")
class Users(Resource):
    @auth_namespace.doc(description="""사용자를 조화하는 API입니다.""")
    @auth_namespace.expect(resource_parser)
    @auth_namespace.marshal_with(fields=user_model, as_list=True)
    @jwt_required()
    def get(self):
        """사용자 조회"""

        user = User.query.get(ident=get_jwt_identity())
        user = user.serialize()
        return user