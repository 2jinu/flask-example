from my_app import create_app, sock

app = create_app()

if __name__ == "__main__":
    # app.run(host="0.0.0.0")
    sock.run(app=app, host="0.0.0.0", allow_unsafe_werkzeug=True)