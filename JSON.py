import json


def readJSON(idServer):  # Reading server playlist data from JSON
    with open('./playlists/playlists.json', 'r') as read_file:
        try:
            return json.load(read_file)[str(idServer)]
        except:
            return {}


def writeJSON(idServer, playlists):  # Writing data from server playlists to JSON
    with open('./playlists/playlists.json', 'r') as read_file: data = json.load(read_file)
    data[str(idServer)] = playlists
    with open('./playlists/playlists.json', 'w') as write_file:
        json.dump(data, write_file)
