import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")

# Fill missing values
movies['genre'] = movies['genre'].fillna('')
movies['overview'] = movies['overview'].fillna('')

# Combine features
movies['tags'] = movies['genre'] + " " + movies['overview']

new_df = movies[['id','title','tags']]

# Convert text to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)

# Save model files
pickle.dump(similarity, open('similarity.pkl','wb'))
pickle.dump(new_df, open('movie_list.pkl','wb'))

print("Model trained successfully!")