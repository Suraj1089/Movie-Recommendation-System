import pickle
import streamlit as st
import requests
import base64
from navbar import *


st.set_page_config(page_title='Movie Recommendation System')


# --- LOAD CSS, PDF & PROFIL PIC ---
with open('static/css/navbar.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

add_cdn_link()
navbar()

@st.experimental_memo
def load_data():
    movies = pickle.load(open('models/view_data.pkl','rb'))
    return movies

movies = load_data()

st.title('Get Movie Details')

choice = st.radio('select',options=['search','show all'])

if choice=='search':
    selected_movie = st.selectbox('Search movie details',
        options=movies['title'].values
    )
    index = movies[movies['title']==selected_movie].index[0]
    
    data = movies.iloc[index-1:index,:]
    st.dataframe(data)

else:
    filter_select = st.multiselect('Filter data :',options=['movie_id','title'])
    
    d = movies.drop('overview',axis=1)
    d = d.sort_values(by=filter_select)
    st.dataframe(d)

