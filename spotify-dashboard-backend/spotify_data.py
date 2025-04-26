import spotipy
from collections import Counter

def get_top_tracks_data(access_token):
    sp = spotipy.Spotify(auth=access_token)
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='long_term')

    if not top_tracks['items']:
        return []

    results = []

    for track in top_tracks['items']:
        results.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "release_date": track['album']['release_date'],
            "duration_minutes": round(track['duration_ms'] / 60000, 2),
            "popularity": track['popularity'],
            "explicit": track['explicit']
        })

    return results


def get_genre_distribution(access_token):
    sp = spotipy.Spotify(auth=access_token)

    # Get top artists (limit can be 10–50)
    top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')

    genre_counter = Counter()
    for artist in top_artists['items']:
        genres = artist.get('genres', [])
        genre_counter.update(genres)

    # Optional: group rare genres into 'Other'
    genre_data = genre_counter.most_common()
    other_total = sum([count for genre, count in genre_data[8:]])  # keep top 7
    top_genres = genre_data[:7]
    if other_total > 0:
        top_genres.append(('Other', other_total))

    return dict(top_genres)

