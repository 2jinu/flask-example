# flask-example

<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" style="width: 100%">

Flask를 사용하여 웹 서비스를 빠르고 쉽게 구축하고 경험할 수 있는 예제 프로젝트를 제공합니다.

| Package               | Description   |
| :---                  | :---          |
| Flask                 | 웹 애플리케이션을 쉽고 빠르게 개발하기 위한 패키지 |
| Flask-WTF             | 폼을 처리하고 유효성을 검사를 수행하는데 도와주는 패키지 |
| Flask-Login           | 사용자 인증 및 세션 관리를 쉽게 구현할 수 있도록 도와주는 패키지 |
| Flask-RESTx           | REST API를 쉽게 개발할 수 있도록 도와주는 패키지 |
| Flask-Caching         | 간단하고 유연한 캐싱 기능을 제공하는 패키지 |
| Flask_SocketIO        | 웹 소켓을 지원하기 위한 패키지 |
| Flask-SQLAlchemy      | 데이터베이스 액세스 툴킷 및 ORM 패키지 |
| Flask-JWT-Extended    | JWT을 구현하고 관리하는 데 사용되는 패키지 |

## Install

docker-compose.yml이 위치한 디렉토리에서 아래의 명령어를 입력하여 컨테이너를 실행할 수 있습니다.

```console
$ docker-compose up
```

데이터베이스 파일들이 존재하지 않을 시, 테이블 및 데이터를 생성하는데

시간이 지연되어 flask 컨테이너로 부터 에러가 출력됩니다.

자동으로 테이블 및 데이터가 생성되고, 약간의 시간이 지난 후 정상적으로 flask가 다시 동작됩니다.

## Connect

터미널에서 아래와 같이 출력된다면 웹 브라우저를 이용하여 `http://{서버 IP}`로 접속하면 로그인 페이지가 출력됩니다.

```
flask      |  * Serving Flask app 'my_app'
flask      |  * Debug mode: on
flask      | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask      |  * Running on all addresses (0.0.0.0)
flask      |  * Running on http://127.0.0.1:5000
flask      |  * Running on http://172.29.0.2:5000
flask      | Press CTRL+C to quit
flask      |  * Restarting with stat
flask      |  * Debugger is active!
flask      |  * Debugger PIN: 448-321-965
```