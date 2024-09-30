<div align="center"><h2>NextBinge - <a href="https://nextbinge.streamlit.app/">Demo</a></h2></div>




https://github.com/user-attachments/assets/2e8b73d2-6f28-401a-8012-8f29a58ddfce




## Overview

NextBinge is a personalized movie recommender system designed to suggest movies similar to the ones you've watched and liked. It leverages content-based filtering, recommending movies by analyzing genres, keywords, cast, and crew information. The system displays movie posters, taglines, genres, and even provides YouTube trailers. It is built using Streamlit for the frontend and leverages machine learning to compute movie similarities, providing a sleek user experience.

## Features

### Movie Recommender
- **Content-Based Filtering:** Recommends movies by comparing similarity tags, including genres, keywords, and cast.
- **Poster and Trailer Display:** Shows movie posters along with taglines, genres, and provides trailers when available.
- **Interactive UI:** Users can select a movie from a dropdown list, and the system generates movie recommendations with an easy-to-use interface.

### Streamlit Frontend
- **Movie Poster Hover Effects:** Smooth hover transitions that display movie titles over posters.
- **Watch Trailers:** Allows users to watch trailers for recommended movies directly from the app using a modal pop-up.
- **Mobile-Friendly:** Responsive design that ensures a consistent experience across devices.

### Machine Learning Model
- **Natural Language Processing (NLP):** Uses stemming, tokenization, and vectorization to convert movie metadata into numerical vectors.
- **Cosine Similarity:** Calculates movie similarity based on their tags and recommends the top 10 closest movies to the selected one.
- **Efficient Data Processing:** Handles a dataset of 4806 movies, computing vector similarities using a Bag of Words model.

## Project Flow

1. **Data Merging:** Combines information from `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` to create a complete dataset.
2. **Data Preprocessing:** Cleans and processes the movie data, including converting lists of genres, keywords, and cast to a unified format.
3. **Model Training:** Utilizes a CountVectorizer to extract the top 5000 features from the movie tags and computes similarities using cosine distance.
4. **Frontend Integration:** Implements a Streamlit app that allows users to generate and view movie recommendations, including trailers and other details.

## Built With

- [![Streamlit][Streamlit-img]][Streamlit-url]
- [![Python][Python-img]][Python-url]
- [![Pandas][Pandas-img]][Pandas-url]
- [![scikit-learn][Sklearn-img]][Sklearn-url]
- [![NLTK][NLTK-img]][NLTK-url]

## How It Works

1. **Data Preprocessing:**
   - The movie and credits datasets are merged to obtain relevant columns such as movie ID, title, genres, keywords, cast, and crew.
   - Lists are extracted from JSON-like strings using `ast.literal_eval`.
   - Text data (genres, keywords, etc.) are processed by removing spaces and applying stemming to normalize the words.

2. **Model Training:**
   - Movie tags are combined into a single string and transformed into a lower-cased, stemmed format.
   - A Bag of Words model is applied to vectorize the tags.
   - Cosine similarity is calculated between the vectors, producing a similarity matrix that is used to recommend movies.

3. **Recommendation System:**
   - When a user selects a movie, the app finds similar movies by calculating the cosine distance to recommend the top 10 closest movies.
   - The app fetches additional details like posters, taglines, genres, and YouTube trailers via the TMDB API.

<!-- MARKDOWN LINKS & IMAGES -->
[Streamlit-img]: https://img.shields.io/badge/Streamlit-black?style=for-the-badge&logo=streamlit
[Streamlit-url]: https://streamlit.io/
[Python-img]: https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Pandas-img]: https://img.shields.io/badge/Pandas-black?style=for-the-badge&logo=pandas
[Pandas-url]: https://pandas.pydata.org/
[Sklearn-img]: https://img.shields.io/badge/scikit--learn-orange?style=for-the-badge&logo=scikit-learn
[Sklearn-url]: https://scikit-learn.org/stable/
[NLTK-img]: https://img.shields.io/badge/NLTK-green?style=for-the-badge&logo=python
[NLTK-url]: https://www.nltk.org/



