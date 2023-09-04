import numpy as np
import pandas as pd
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the similarity matrix from the file
similarity = np.load('Saved Files\similarity.npy',allow_pickle=True)

# Loading the list of movie titles from the file
list_of_all_titles = np.load('Saved Files\list_of_all_titles.npy',allow_pickle=True)

# Load the index_to_title_mapping from the file
index_to_title_mapping = np.load(
    'Saved Files\index_to_title_mapping.npy', allow_pickle=True).item()

# Create a DataFrame from the dictionary
movies_data = pd.DataFrame.from_dict(
    index_to_title_mapping, orient='index', columns=['title'])


@app.get("/recommend/")
async def get_movie_recommendations(movie_name: str):
    print(movie_name)
    # finding the close match for the movie name given by the user
    find_close_match = difflib.get_close_matches(
        movie_name, list_of_all_titles)
    close_match = find_close_match[0]

    index_of_the_movie = movies_data[movies_data['title']
                                     == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    # sorting the movies based on their similarity score
    sorted_similar_movies = sorted(
        similarity_score, key=lambda x: x[1], reverse=True)

    recommendations = []

    for i, movie in enumerate(sorted_similar_movies):
        index = int(movie[0])
        if i == 0:
            continue
        if i < 5:  # Get top 5 similar movies
            title_from_index = movies_data.iloc[index]['title']
            similarity_score = movie[1]
            recommendation = {
                "Rank": i,
                "Title": title_from_index,
                "Similarity_Score": similarity_score
            }
            recommendations.append(recommendation)

    response_data = json.dumps(recommendations)
    response = Response(content=response_data, media_type="application/json")
    response.headers["Access-Control-Allow-Origin"] = origins[0]  # Allow the specific origin

    return recommendations
