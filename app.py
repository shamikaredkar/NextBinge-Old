import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ec3d3f78a72c37231a2bd59e1bed0bb5&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # Get tagline
    tagline = data.get('tagline', 'No tagline available.')
    
    # Get genres
    genres = [genre['name'] for genre in data.get('genres', [])]
    genres_str = ", ".join(genres) if genres else 'No genres available.'
    return full_path, tagline, genres_str

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_taglines = []
    recommended_movie_genres = []
    
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, tagline, genres = fetch_poster(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_taglines.append(tagline)
        recommended_movie_genres.append(genres)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_taglines, recommended_movie_genres


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values


# Add custom CSS for hover effect
st.markdown("""
    <style>
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
    </style>
""", unsafe_allow_html=True)


st.title("NextBinge")
option = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_taglines, recommended_movie_genres = recommend(option)
    
    # First row of 5 columns
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

    # Second row of 5 columns
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