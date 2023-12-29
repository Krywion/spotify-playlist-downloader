import time

from flask import Flask, render_template, request, redirect
from flask import session, send_file, jsonify
from flask_wtf import CSRFProtect

from searchForm import SearchForm
from apscheduler.schedulers.background import BackgroundScheduler

import shutil
import spotifyAPI
import youtubeDownloader

from youtubeDownloader import current_progress

app = Flask(__name__)
app.secret_key = "secret_key"
csrf = CSRFProtect(app)


def sensor():
    print("Scheduler is alive!")


scheduler = BackgroundScheduler(deamon=True)
scheduler.add_job(youtubeDownloader.clean_files, 'interval', seconds=60)
scheduler.start()


@app.route("/")
def index():
    form = SearchForm()
    loginUrl = spotifyAPI.login()
    return render_template("index.html", loginUrl=loginUrl, form=form)


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


@app.route("/search-playlist", methods=['POST'])
def search_playlist():
    url = request.form['search_query']
    print("URL: " + url)
    playlist_id = spotifyAPI.get_playlist_id(url)
    token = spotifyAPI.get_token()
    tracks = spotifyAPI.get_tracks(token, playlist_id)
    return render_template("tracks.html", tracks=tracks, playlist_id=playlist_id)


@app.route("/tracks/<playlist_id>")
def tracks(playlist_id):
    token = session['token']
    tracks = spotifyAPI.get_tracks(token, playlist_id)
    return render_template("tracks.html", playlist_id=playlist_id, tracks=tracks)


@app.route("/download/<playlist_id>")
def download(playlist_id):
    token = session['token']
    print("Playlist ID: " + playlist_id)
    tracks = spotifyAPI.get_tracks(token, playlist_id)
    names = []
    for track in tracks:
        names.append(track.artist + " " + track.name)

    zip_loc = "../music/" + playlist_id
    zip_dest = "../music/" + playlist_id

    youtubeDownloader.download_music(names, playlist_id)
    shutil.make_archive(zip_loc, 'zip', zip_dest)
    return send_file("../music/" + playlist_id + ".zip", as_attachment=True)

@app.route('/long-polling-progress/<playlist_id>')
def long_polling_progress(playlist_id):
    start_time = time.time()
    timeout = 20  # Ustawienie limitu czasowego

    while True:
        # Zakładamy, że `get_current_progress` zwraca postęp dla danego playlist_id
        progress = youtubeDownloader.get_current_progress(playlist_id)

        if progress is not None:
            return jsonify({'progress': progress})

        # Sprawdzenie, czy nie upłynął limit czasu
        if time.time() - start_time > timeout:
            break

        time.sleep(1)  # Krótkie opóźnienie, aby uniknąć zbyt częstego odpytywania

    return jsonify({'progress': 'timeout'})


if __name__ == "__main__":
    app.run(debug=True, port=int("8080"), host="0.0.0.0", use_reloader=False)
