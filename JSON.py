import json


def readJSON(idServer):
    with open('./playlists/playlists.json', 'r') as read_file:
        return json.load(read_file)[str(idServer)]


def writeJSON(idServer, playlists):
    data = readJSON(idServer)
    data[str(idServer)] = playlists
    with open('./playlists/playlists.json', 'w') as write_file:
        json.dump(data, write_file)
