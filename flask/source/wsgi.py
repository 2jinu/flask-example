from my_app import create_app, sock

app = create_app()

if __name__ == "__main__":
    sock.run(app=app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)