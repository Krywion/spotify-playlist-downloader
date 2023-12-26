from flask import Flask, render_template, request, redirect
from flask import session, send_file
from apscheduler.schedulers.background import BackgroundScheduler

import shutil
import spotifyAPI
import youtubeDownloader

app = Flask(__name__)
app.secret_key = "super secret key"


def sensor():
    print("Scheduler is alive!")


scheduler = BackgroundScheduler(deamon=True)
scheduler.add_job(youtubeDownloader.clean_files, 'interval', seconds=60)
scheduler.start()


@app.route("/")
def index():
    loginUrl = spotifyAPI.login()
    return render_template("index.html", loginUrl=loginUrl)


@app.route("/callback")
def callback():
    code = request.args.get('code')
    token = spotifyAPI.client_auth(code)
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


@app.route("/tracks/<playlist_id>")
def tracks(playlist_id):
    token = session['token']
    tracks = spotifyAPI.get_tracks(token, playlist_id)
    return render_template("tracks.html", playlist_id=playlist_id, tracks=tracks)


@app.route("/download/<playlist_id>")
def download(playlist_id):
    token = session['token']
    tracks = spotifyAPI.get_tracks(token, playlist_id)
    names = []
    for track in tracks:
        names.append(track.artist + " " + track.name)
    youtubeDownloader.download_music(names, playlist_id)
    zip_loc = "../music/" + playlist_id
    zip_dest = "../music/" + playlist_id
    shutil.make_archive(zip_loc, 'zip', zip_dest)
    return send_file("../music/" + playlist_id + ".zip", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=int("8080"), host="0.0.0.0", use_reloader=False)
