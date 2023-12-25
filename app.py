from flask import Flask, render_template, request, make_response, redirect
from flask import session

import spotifyAPI

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    loginUrl = spotifyAPI.login()
    return render_template("index.html", loginUrl=loginUrl)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token = spotifyAPI.client_auth(code)
    print(token)
    session.pop('token', None)
    session['token'] = token
    return redirect("/user")

@app.route("/user")
def user():
    token = session['token']
    username = spotifyAPI.get_username(token)
    return render_template("user.html", username=username)

@app.route("/playlists")
def playlists():
    token = session['token']
    playlists = spotifyAPI.get_playlists(token)
    return render_template("playlists.html", playlists=playlists)


if __name__ == "__main__":
    app.run(debug=True, port=8080)