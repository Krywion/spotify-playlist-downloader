docker build -t krywion/spotify-app:0.0.1.RELESE .
docker stop krywion/spotify-app:0.0.1.RELESE
docker rm krywion/spotify-app:0.0.1.RELESE
docker run -d -p 8080:8080 krywion/spotify-app:0.0.1.RELESE