import streamlit as st
import pandas as pd
import pickle
import scipy.sparse as sp
import requests

# ==== ABSOLUTE PATH ====
BASE = "C:/Users/hp/OneDrive/Desktop/movie-recommender/backend/artifacts/"

df = pd.read_pickle(BASE + "movies_df.pkl")

with open(BASE + "tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

tfidf_matrix = sp.load_npz(BASE + "tfidf_matrix.npz")

OMDB_API_KEY = "a103b426"

# ==== Utility: Fetch poster by title ====
def get_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster = data.get("Poster")
    if poster and poster != "N/A":
        return poster
    return "https://via.placeholder.com/300x450?text=No+Image"

# ==== Recommend movies ====
def recommend(movie, n=10):
    if movie not in df['primaryTitle'].values:
        return []

    idx = df[df['primaryTitle'] == movie].index[0]
    from sklearn.metrics.pairwise import linear_kernel
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = sim_scores.argsort()[::-1][1:n+1]

    movies = []
    for i in similar_indices:
        row = df.iloc[i]
        poster = get_poster(row['primaryTitle'])
        movies.append((row['primaryTitle'], poster, row['genres'], row['averageRating']))

    return movies

# ==== CSS Styling & Animations ====
st.markdown("""
<style>
/* ===== Semi-Transparent Grey Background ===== */
[data-testid="stAppViewContainer"], 
[data-testid="stMainContainer"], 
[data-testid="stSidebar"] {
    background: rgba(128,128,128,0.5) !important;
}

/* For older Streamlit versions */
.css-18e3th9 {
    background: rgba(128,128,128,0.5) !important;
}

/* ===== Animated Title ===== */
@keyframes titleGradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.animated-title {
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(270deg, #ff416c, #ff4b2b, #f9d423, #ff416c);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGradient 8s ease infinite;
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 0 0 6px rgba(255,69,0,0.5);
}

/* ===== Animated Selectbox Label ===== */
@keyframes selectGradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.animated-label {
    font-weight: bold;
    background: linear-gradient(270deg, #ff416c, #ff4b2b, #f9d423, #ff416c);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: selectGradient 6s ease infinite;
    text-shadow: 0 0 4px rgba(255,69,0,0.5);
}

/* ===== Animated Placeholder ===== */
.stSelectbox [data-baseweb="select"] > div > div > div > div > span:first-child {
    font-weight: bold;
    background: linear-gradient(270deg, #ff416c, #ff4b2b, #f9d423, #ff416c);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: selectGradient 6s ease infinite;
    text-shadow: 0 0 4px rgba(255,69,0,0.5);
}

/* ===== Movie Cards ===== */
@keyframes fireGlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.movie-card {
    background: linear-gradient(270deg, #ff416c, #ff4b2b, #f9d423, #ff416c);
    background-size: 600% 600%;
    animation: fireGlow 8s ease infinite;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 20px;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 390px;
}
.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(255,69,0,0.8);
}
.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    margin: 5px 0 2px 0;
    text-align: center;
}
.movie-info {
    font-size: 13px;
    color: #ffffff;
    text-align: center;
    word-wrap: break-word;
}
.movie-poster {
    width: 180px;
    height: 270px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

/* ===== Footer Styling ===== */
.footer {
    width: 100%;
    background: rgba(17, 17, 17, 0.8);
    padding: 30px 20px;
    margin-top: 50px;
    text-align: center;
    color: #ddd;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: background 0.3s, box-shadow 0.3s;
}
.footer:hover {
    background: rgba(17, 17, 17, 1);
    box-shadow: 0 4px 20px rgba(255,69,0,0.3);
}

.footer-logo {
    font-size: 24px;
    color: #ff4b2b;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.footer-text {
    font-size: 14px;
    color: #fff;
    line-height: 1.6;
    max-width: 1200px;
    margin: 0 auto;
}

.footer-text b.navin {
    font-weight: 700;
    cursor: pointer;
    color: #ff4b2b;
    background: linear-gradient(45deg, #ff4b2b, #ff8c00, #f9d423, #ff4b2b);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fireFlicker 2s infinite;
}

@keyframes fireFlicker {
    0%   {background-position:0% 50%; text-shadow: 0 0 4px #ff416c, 0 0 8px #ff4b2b;}
    25%  {background-position:50% 50%; text-shadow: 0 0 6px #ff416c, 0 0 10px #ff4b2b;}
    50%  {background-position:100% 50%; text-shadow: 0 0 4px #f9d423, 0 0 12px #ff4b2b;}
    75%  {background-position:50% 50%; text-shadow: 0 0 8px #ff416c, 0 0 14px #ff4b2b;}
    100% {background-position:0% 50%; text-shadow: 0 0 6px #ff416c, 0 0 10px #ff4b2b;}
}

.footer-text a {
    text-decoration: none;
    color: #ff4b2b;
    transition: color 0.3s;
}
.footer-text a:hover {
    color: #ffa500;
}

.footer-separator {
    width: 50px;
    height: 2px;
    background: #ff4b2b;
    margin: 12px auto;
    border-radius: 2px;
}

/* Icons */
.footer-icons {
    margin-top: 12px;
}
.footer-icons a {
    display: inline-block;
    margin: 0 10px;
    transition: transform 0.3s, filter 0.3s;
}
.footer-icons a:hover {
    transform: scale(1.2);
    filter: brightness(1.5);
}
.footer-icons a.github img {
    filter: invert(50%) sepia(100%) saturate(500%) hue-rotate(10deg) brightness(1.3);
    transition: filter 0.3s;
}
.footer-icons a.github:hover img {
    filter: invert(0%) sepia(100%) saturate(800%) hue-rotate(10deg) brightness(1.6);
}
.footer-icons img {
    width: 28px;
    height: 28px;
}
</style>
""", unsafe_allow_html=True)

# ==== Page UI ==== #
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Animated title
st.markdown('<h1 class="animated-title">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)

# Animated label
st.markdown('<label class="animated-label">Select a movie:</label>', unsafe_allow_html=True)

# Movie list 
movie_list = ["Please choose the movie..!"] + df['primaryTitle'].tolist()
selected_movie = st.selectbox("", movie_list, index=0)

# Recommendation button with warning
if st.button("Get Recommendations"):
    if selected_movie == "Please choose the movie..!":
        st.warning("⚠️ Please choose a movie before getting recommendations!")
    else:
        results = recommend(selected_movie)
        num_cols = 5
        with st.container():
            for i in range(0, len(results), num_cols):
                cols = st.columns(num_cols, gap="large")
                for j, (title, poster, genres, rating) in enumerate(results[i:i+num_cols]):
                    with cols[j]:
                        youtube_search = f"https://www.youtube.com/results?search_query={title}+official+trailer"
                        st.markdown(f"""
                        <a href="{youtube_search}" target="_blank" style="text-decoration:none;">
                            <div class='movie-card'>
                                <img class='movie-poster' src="{poster}">
                                <p class='movie-title'>{title}</p>
                                <p class='movie-info'>⭐ {rating} | {genres}</p>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)

# ==== Footer ====
st.markdown("""
<div class="footer">
    <div class="footer-logo">MOVIES BASED</div>
    <div class="footer-separator"></div>
    <div class="footer-text">
        All recommendations are generated using <b>TF-IDF similarity</b>.<br>
        Designed by <b class="navin">Navin Raj</b> • <a href="#">Movie Recommender App</a>
    </div>
    <div class="footer-icons">
        <a href="mailto:kumarnavin9316@gmail.com" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email">
        </a>
        <a href="https://www.linkedin.com/in/navin-kumar-744681264" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">
        </a>
        <a href="https://github.com/mrnavinkr" target="_blank" class="github">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub">
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
