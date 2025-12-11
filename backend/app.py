from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import scipy.sparse as sp
from sklearn.metrics.pairwise import linear_kernel
from difflib import get_close_matches
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend or Streamlit

# Your TMDb API Key
TMDB_API_KEY = "a103b426"  # Replace with your actual TMDb key if different

# Load artifacts
df = pd.read_pickle("artifacts/movies_df.pkl")
with open("artifacts/tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)
tfidf_matrix = sp.load_npz("artifacts/tfidf_matrix.npz")

# Index mapping
indices = pd.Series(df.index, index=df['primaryTitle']).drop_duplicates()

def find_title(query):
    """Find exact or close match for movie title"""
    if query in indices:
        return query
    lower_map = {t.lower(): t for t in indices.index}
    if query.lower() in lower_map:
        return lower_map[query.lower()]
    close = get_close_matches(query, indices.index, n=1, cutoff=0.6)
    return close[0] if close else None

def get_tmdb_poster(title):
    """Fetch poster from TMDb using movie title"""
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        r = requests.get(url)
        data = r.json()
        if data['results']:
            path = data['results'][0].get('poster_path')
            if path:
                return f"https://image.tmdb.org/t/p/w500{path}"
        return "https://via.placeholder.com/150"
    except:
        return "https://via.placeholder.com/150"

@app.route("/")
def home():
    return "Movie Recommendation API is running. Use /api/recommend?title=MovieName"

@app.route("/api/recommend")
def recommend():
    title = request.args.get("title", "")
    n = int(request.args.get("n", 9))
    if not title:
        return jsonify({"error": "title query param required"}), 400

    matched = find_title(title)
    if not matched:
        return jsonify({"error": "Movie not found"}), 404

    idx = indices[matched]
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    related_idx = sim_scores.argsort()[::-1][1:n+1]

    results = []
    for i in related_idx:
        row = df.iloc[i]
        genres_clean = [g.strip() for g in row['genres'].split("|")] if row['genres'] else []
        poster_url = get_tmdb_poster(row['primaryTitle'])
        results.append({
            "title": row['primaryTitle'],
            "genres": genres_clean,
            "averageRating": float(row['averageRating']),
            "numVotes": int(row['numVotes']),
            "poster": poster_url
        })

    return jsonify({"query": matched, "recommendations": results})

if __name__ == "__main__":
    app.run(debug=True)
