import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.neighbors import NearestNeighbors
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample Song Data (Simulated Features)
songs_data = pd.DataFrame({
    'song_id': [1, 2, 3, 4, 5],
    'song_name': ['Song A', 'Song B', 'Song C', 'Song D', 'Song E'],
    'genre': ['Pop', 'Pop', 'Rock', 'Pop', 'Rock'],
    'artist': ['Artist X', 'Artist Y', 'Artist X', 'Artist Z', 'Artist X'],
    'duration': [210, 230, 190, 250, 240],  # Duration in seconds
})

# Simulate feature vector (genre, artist, duration as features)
songs_data['genre_code'] = pd.Categorical(songs_data['genre']).codes
songs_data['artist_code'] = pd.Categorical(songs_data['artist']).codes
X = songs_data[['genre_code', 'artist_code', 'duration']].values  # Features

# Fit a KNN model to recommend songs based on similarity
knn = NearestNeighbors(n_neighbors=3, algorithm='auto')
knn.fit(X)

# Pydantic Models for Request/Response
class RecommendationRequest(BaseModel):
    song_id: int

class RecommendationResponse(BaseModel):
    recommendations: list

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_songs(request: RecommendationRequest):
    song_id = request.song_id

    # Find the song features by song_id
    song_features = songs_data[songs_data['song_id'] == song_id][['genre_code', 'artist_code', 'duration']].values

    # Get recommendations based on KNN
    distances, indices = knn.kneighbors(song_features)

    # Get the recommended song names
    recommended_songs = []
    for idx in indices[0]:
        recommended_song = songs_data.iloc[idx]['song_name']
        recommended_songs.append(recommended_song)

    return {"recommendations": recommended_songs}

