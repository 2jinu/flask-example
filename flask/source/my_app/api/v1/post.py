from json import dumps
from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, fields

from my_app.models.post import Post

post_namespace = Namespace(name="posts", description="Post API")

post_model = post_namespace.model(name="게시글 모델", model={
    "id": fields.String(description="게시글 식별 값"),
    "title": fields.String(description="게시글 제목"),
    "content": fields.String(description="게시글 내용"),
    "username" : fields.String(description="게시글 글쓴이"),
    "created" : fields.String(description="게시글 작성 일시"),
    "views" : fields.String(description="게시글 조회수"),
})
error_message = post_namespace.model(name="오류 메시지 모델", model={
    "msg" : fields.String(description="오류 내용")
})
 
@post_namespace.route("")
class Posts(Resource):
    @post_namespace.doc(description="""게시글을 조화하는 API입니다.""", security="apikey")
    @post_namespace.response(code=200, description="게시글 정보", model=[post_model])
    @post_namespace.response(code=401, description="API key가 존재하지 않습니다.", model=error_message)
    @post_namespace.response(code=403, description="허용되지 않은 API key입니다.", model=error_message)
    def get(self):
        """사용자 조회"""

        if not "X-API-KEY" in request.headers:
            return make_response(jsonify(msg="API key is missing"), 401)
        
        api_key = request.headers.get(key="X-API-KEY", default="")
        if "myapikey" != api_key:
            return make_response(jsonify(msg="Invalid API key"), 403)

        posts = Post.query.order_by(Post.created.desc()).all()
        posts = [post.serialize() for post in posts]
        return posts