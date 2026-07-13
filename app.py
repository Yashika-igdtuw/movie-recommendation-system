import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.title("🎥 Movie Recommender")
    st.write("Content Based Movie Recommendation System")
    st.markdown("---")
    st.write("Built using:")
    st.write("✅ Python")
    st.write("✅ Pandas")
    st.write("✅ Scikit-Learn")
    st.write("✅ Streamlit")
    st.write("✅ TMDB API")

# ---------------- FETCH POSTER ---------------- #

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=017b902df811d234cf47f74f1baeb4d3&language=en-US"

    data = requests.get(url)

    if data.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    data = data.json()

    poster_path = data.get("poster_path")

    if poster_path is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500/" + poster_path


# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


# ---------------- LOAD DATA ---------------- #

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- TITLE ---------------- #

st.title("🎬 Movie Recommendation System")

st.write(
    "Select a movie and discover five similar movies instantly."
)

selected_movie_name = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

# ---------------- BUTTON ---------------- #

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):

        names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
    "<center>Made with ❤️ by Yashika</center>",
    unsafe_allow_html=True
)