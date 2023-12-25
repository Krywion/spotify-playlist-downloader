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
    state = request.args.get('state')
    print("Code:", code)  # Debugowanie
    print("State:", state)  # Debugowanie
    session['code'] = code
    return redirect("/user")

@app.route("/user")
def user():
    code = session['code']
    print(code)
    username = spotifyAPI.get_username(code)
    return render_template("user.html", username=username)


if __name__ == "__main__":
    app.run(debug=True, port=8080)