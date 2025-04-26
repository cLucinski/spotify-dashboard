import spotipy

def get_top_tracks(access_token):
    sp = spotipy.Spotify(auth=access_token)
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')

    if not top_tracks['items']:
        return []

    results = []
    for track in top_tracks['items']:
        results.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "popularity": track['popularity'],
            "album": track['album']['name'],
            "release_date": track['album']['release_date']
        })

    return results
