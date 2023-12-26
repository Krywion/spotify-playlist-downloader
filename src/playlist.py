class Playlist:
    def __init__(self,id, name, url, owner):
        self.name = name
        self.id = id
        self.url = url
        self.owner = owner

class Track:
    def __init__(self, id, name, url, artist):
        self.name = name
        self.id = id
        self.url = url
        self.artist = artist

