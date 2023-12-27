docker build -t krywion/spotify-app:0.0.1.RELESE .
docker stop spotifyApp
docker rm spotifyApp
docker run --name spotifyApp -d -p 8080:8080 krywion/spotify-app:0.0.1.RELESE