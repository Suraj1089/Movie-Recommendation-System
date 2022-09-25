import pickle
import streamlit as st
import requests
import base64
from navbar import *
from dotenv import load_dotenv
import os 

st.set_page_config(page_title='Movie Recommendation System')

#load environment variables
load_dotenv(".env")
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')

# --- LOAD CSS, PDF & PROFIL PIC ---
with open('static/css/navbar.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

#import navbar 
add_cdn_link()
navbar()

@st.experimental_memo
def load_data():
    movies = pickle.load(open('models/model.pkl','rb'))
    similarity = pickle.load(open('models/similar.pkl','rb'))
    return movies,similarity

movies,similarity = load_data()

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US".format(movie_id,MOVIE_API_KEY)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    overview = data['release_date']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,overview

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overview = []

    for i in distances[1:15]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id)[0])
        recommended_movie_overview.append(fetch_poster(movie_id)[1])
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters,recommended_movie_overview


st.header('Movie Recommender System')




movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters,recommended_movie_overview = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(recommended_movie_names[0])
        st.write(recommended_movie_overview[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.text(recommended_movie_overview[0])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.text(recommended_movie_overview[0])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.text(recommended_movie_overview[0])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.text(recommended_movie_overview[0])
        st.image(recommended_movie_posters[4])




