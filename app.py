from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):

    movie = movie.lower()

    matches = movies[movies['title'].str.lower().str.contains(movie)]

    if matches.empty:
        return ["Movie not found"]

    index = matches.index[0]

    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True,
                       key=lambda x: x[1])

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


@app.route("/", methods=["GET","POST"])
def home():

    recommendations = []

    if request.method == "POST":
        movie = request.form.get("movie")
        recommendations = recommend(movie)

    return render_template("index.html",
                           recommendations=recommendations)


# API for autocomplete
@app.route("/search")
def search():

    query = request.args.get("q")

    if query:
        results = movies[movies['title'].str.lower().str.contains(query.lower())]
        movie_list = results['title'].head(5).tolist()
        return jsonify(movie_list)

    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)