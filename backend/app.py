import pandas as pd

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# Reads the CSV file

app = Flask(__name__)
CORS(app)

df = pd.read_csv('data\imdb_top_1000.csv')



# Create a TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')
df['Overview'] = df['Overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['Overview'])


# Use cosine to find similarity between movies
sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
@app.route('/')
def home():
    return render_template('index.html')

def recommend_movies(title, df, sim_matrix):
    try:
        if title not in df['Series_Title'].values:
            return ["Movie not found. Try another movie."]
    
        idx = df[df['Series_Title'] == title].index[0] # Get the index of the movie
        scores = list(enumerate(sim_matrix[idx])) # Get the similarity scores for the movie
        scores = sorted(scores, key=lambda x: x[1], reverse=True) # Format for highest scores

        movies = [df.iloc[i[0]]['Series_Title'] for i in scores] # Get all the movies 
        return movies[:5]
    
    except Exception as e:
        return jsonify(f'Error: {str(e)}'), 500


    

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        title = data.get('title', '')
        recommendations = recommend_movies(title, df, sim_matrix)
        if(recommendations == '500'):
            return jsonify('Error in getting recommendations')
        else:
            return jsonify(recommendations)
    
    except Exception as e:
        return jsonify(f'Error: {str(e)}'), 500
    

if __name__ == '__main__':
    app.run(debug=True)