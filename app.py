import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


def page_one():
    st.title("MUSIC")

    CLIENT_ID = "5873617a74a64a28ac2ed070e9fcc978"
    CLIENT_SECRET = "962a26a2e387428c94de55a0c49753fd"

    # Initialize the Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_song_album_cover_url(song_name, artist_name):
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track")

        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            album_cover_url = track["album"]["images"][0]["url"]
            print(album_cover_url)
            return album_cover_url
        else:
            return "https://i.postimg.cc/0QNxYz4V/social.png"

    def recommend(song):
        index = music[music['song'] == song].index[0]
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_music_names = []
        recommended_music_posters = []
        for i in distances[1:11]:
            # fetch the movie poster
            artist = music.iloc[i[0]].artist
            print(artist)
            print(music.iloc[i[0]].song)
            recommended_music_posters.append(
                get_song_album_cover_url(music.iloc[i[0]].song, artist))
            recommended_music_names.append(music.iloc[i[0]].song)

        return recommended_music_names, recommended_music_posters

    st.header('Recommendation System')
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    music_list = music['song'].values
    selected_movie = st.selectbox(
        "Type or select a song from the dropdown",
        music_list
    )

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters = recommend(
            selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_music_names[0])
            st.image(recommended_music_posters[0])
        with col2:
            st.text(recommended_music_names[1])
            st.image(recommended_music_posters[1])

        with col3:
            st.text(recommended_music_names[2])
            st.image(recommended_music_posters[2])
        with col4:
            st.text(recommended_music_names[3])
            st.image(recommended_music_posters[3])
        with col5:
            st.text(recommended_music_names[4])
            st.image(recommended_music_posters[4])

        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            st.text(recommended_music_names[5])
            st.image(recommended_music_posters[5])
        with col7:
            st.text(recommended_music_names[6])
            st.image(recommended_music_posters[6])

        with col8:
            st.text(recommended_music_names[7])
            st.image(recommended_music_posters[7])
        with col9:
            st.text(recommended_music_names[8])
            st.image(recommended_music_posters[8])
        with col10:
            st.text(recommended_music_names[9])
            st.image(recommended_music_posters[9])


def page_two():
    st.title("MOVIE")

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f08c21ed14fe6e0b5a794d8f478b49e4&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:11]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters

    st.header('Recommendation System')
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(
        open('similarity_movie.pkl', 'rb'))

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie)

        cols = st.columns(5)
        for i in range(10):
            with cols[i % 5]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])


page = st.sidebar.radio("Select a page", ["MUSIC", "MOVIE"])

if page == "MUSIC":
    page_one()
elif page == "MOVIE":
    page_two()
