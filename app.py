import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_modal import Modal

# Add combined custom CSS for hover effect and hiding modal "X" button
st.markdown("""
    <style>
    /* Hover effect for movie posters */
    .movie-container {
        position: relative;
        width: 100%;
    }
    .movie-title {
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        color: white;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 5px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .movie-container:hover .movie-title {
        opacity: 1;
    }
    .movie-poster {
        width: 100%;
        height: auto;
    }
    
    /* Hide modal close (X) button */
    .modal-header button.close {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Function to fetch poster, tagline, genres, and trailer URL
def fetch_poster_and_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec3d3f78a72c37231a2bd59e1bed0bb5&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
    tagline = data.get('tagline', 'No tagline available.')
    genres = [genre['name'] for genre in data.get('genres', [])]
    genres_str = ", ".join(genres) if genres else 'No genres available.'

    trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=ec3d3f78a72c37231a2bd59e1bed0bb5&language=en-US"
    trailer_data = requests.get(trailer_url).json()

    trailer = None
    if trailer_data['results']:
        for video in trailer_data['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer = f"https://www.youtube.com/watch?v={video['key']}"
                break

    return full_path, tagline, genres_str, trailer

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_taglines = []
    recommended_movie_genres = []
    recommended_movie_trailers = []
    
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, tagline, genres, trailer = fetch_poster_and_trailer(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_taglines.append(tagline)
        recommended_movie_genres.append(genres)
        recommended_movie_trailers.append(trailer)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_taglines, recommended_movie_genres, recommended_movie_trailers

# Load movie data and similarity model
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Initialize session state for recommendations and modal control
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'trailer_url' not in st.session_state:
    st.session_state.trailer_url = None
if 'modal_open' not in st.session_state:
    st.session_state.modal_open = False  # Control for modal state

st.title("NextBinge")
movie_list = movies['title'].values
option = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    # Get recommendations and store them in session state
    st.session_state.recommendations = recommend(option)

# Display recommendations if available in session state
if st.session_state.recommendations:
    recommended_movie_names, recommended_movie_posters, recommended_movie_taglines, recommended_movie_genres, recommended_movie_trailers = st.session_state.recommendations
    
    # Display first row of 5 movies
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f"""
            <div class="movie-container">
                <img class="movie-poster" src="{recommended_movie_posters[i]}" alt="{recommended_movie_names[i]}">
                <div class="movie-title">{recommended_movie_names[i]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(recommended_movie_taglines[i])
            st.caption(f"Genres: {recommended_movie_genres[i]}")
            if recommended_movie_trailers[i]:
                if st.button(f'Watch Trailer', key=f'trailer_button_{i}'):
                    st.session_state.trailer_url = recommended_movie_trailers[i]
                    st.session_state.modal_open = True  # Set modal state to open

    # Display second row of 5 movies
    col6, col7, col8, col9, col10 = st.columns(5)
    for i, col in enumerate([col6, col7, col8, col9, col10], start=5):
        with col:
            st.markdown(f"""
            <div class="movie-container">
                <img class="movie-poster" src="{recommended_movie_posters[i]}" alt="{recommended_movie_names[i]}">
                <div class="movie-title">{recommended_movie_names[i]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(recommended_movie_taglines[i])
            st.caption(f"Genres: {recommended_movie_genres[i]}")
            if recommended_movie_trailers[i]:
                if st.button(f'Watch Trailer', key=f'trailer_button_{i}'):
                    st.session_state.trailer_url = recommended_movie_trailers[i]
                    st.session_state.modal_open = True  # Set modal state to open

# Modal setup
modal = Modal(key="TrailerModal", title="Movie Trailer")

# Only open the modal if the button was clicked
if st.session_state.modal_open:
    with modal.container():
        if st.session_state.trailer_url:
            st.video(st.session_state.trailer_url)
        if st.button("Close Trailer"):
            st.session_state.modal_open = False  # Close the modal when button is clicked
            st.experimental_rerun()  # Rerun the app to reflect the modal state change
