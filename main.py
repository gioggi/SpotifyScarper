# Shows the list of all songs sung by the artist or the band
import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from writer import Writer

logger = logging.getLogger('examples.artist_discography')
logging.basicConfig(level='INFO')


def get_args():
    parser = argparse.ArgumentParser(description='Shows albums and tracks for '
                                                 'given artist')
    parser.add_argument('-al', '--artistList', required=True,
                        help='Artist list txt or csv')
    parser.add_argument('-fA', '--fileNameArtist', required=False,
                        help='Artist file name for output')
    parser.add_argument('-fT', '--fileNameTrack', required=False,
                        help='Track file name for output')
    parser.add_argument('-no-f', '--noFile', required=False,
                        help="Don't save the output")
    return parser.parse_args()


def read_file(file_name):
    with open(file_name, 'r') as file:
        artist_line = file.readline()
        artist = get_artist(artist_line)
        save_artist(artist)
        show_artist_albums(artist)
        cnt = 1
        while artist_line:
            print("Line {}: {}".format(cnt, artist_line.strip()))
            artist_line = file.readline()
            artist = get_artist(artist_line)
            save_artist(artist)
            show_artist_albums(artist)
            cnt += 1


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist', market='IT')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def save_album_tracks(album, artist_id):
    tracks = []
    results = sp.album_tracks(album['id'])
    album_release_date = album['release_date']
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for i, album_track in enumerate(tracks):
        album_id = album['id']
        track = sp.track(album_track['id'])
        audio_features = sp.audio_features([track['id']])
        save_track(track, artist_id, album_id, album_release_date, audio_features)


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    logger.info('Total albums: %s', len(albums))
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            logger.info('ALBUM: %s', name)
            unique.add(name)
            save_album_tracks(album, artist['id'])


def save_artist(artist):
    try:
        artist_row = [artist['id'], artist['name'], artist['popularity'], artist['followers']['total']]
        if len(artist['genres']) > 0:
            genres = ','.join(artist['genres'])
            artist_row.append(genres)
        else:
            artist_row.append('')
        writer_artist.write_row(artist_row)
    except:
        print("TypeError ")


def save_track(track, artist_id, album_id, album_release_date, audio_features):
    try:
        track_row = [
            track['id'],
            artist_id,
            album_id,
            album_release_date,
            track['name'],
            track['disc_number'],
            track['duration_ms'],
            track['explicit'],
            track['popularity'],
            track['track_number'],
            audio_features[0]['danceability'],
            audio_features[0]['energy'],
            audio_features[0]['key'],
            audio_features[0]['loudness'],
            audio_features[0]['mode'],
            audio_features[0]['speechiness'],
            audio_features[0]['acousticness'],
            audio_features[0]['instrumentalness'],
            audio_features[0]['liveness'],
            audio_features[0]['valence'],
            audio_features[0]['tempo'],
            audio_features[0]['time_signature']
        ]
        writer_track.write_row(track_row)
    except:
        print("TypeError ")



def main():
    read_file(args.artistList)


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    args = get_args()
    if args.fileNameArtist:
        writer_artist = Writer(args.fileNameArtist)
    else:
        writer_artist = Writer()
    if args.fileNameTrack:
        writer_track = Writer(file_name=args.fileNameTrack, writer_type='track')
    else:
        writer_track = Writer(writer_type='track')
    main()
