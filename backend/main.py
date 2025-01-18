import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.neighbors import NearestNeighbors
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS Middleware to allow frontend calls
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

class ChatRequest(BaseModel):
    query: str

# Endpoint to recommend songs
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

# Endpoint to handle chatbot queries
@app.post("/chatbot")
async def handle_chatbot_query(request: ChatRequest):
    user_query = request.query.lower()

    # If the query asks for song recommendations, process the song ID
    if "recommend" in user_query or "song" in user_query:
        # Extract song ID from user query (you can improve this regex if needed)
        song_id = None
        for word in user_query.split():
            if word.isdigit():  # Check if there's a number (song ID) in the query
                song_id = int(word)
                break

        if song_id and song_id in songs_data['song_id'].values:
            # Call recommendation endpoint
            recommended_songs = await recommend_songs(RecommendationRequest(song_id=song_id))
            recommendations = recommended_songs['recommendations']
            return {"response": f"Here are some recommendations for Song ID {song_id}: {', '.join(recommendations)}"}
        else:
            return {"response": "Sorry, I couldn't find a valid song ID in your query. Please provide a valid song ID."}
    
    elif "thank you" in user_query:
        return {"response": "You're welcome! Let me know if you need any more recommendations."}
    
    else:
        return {"response": "Sorry, I didn't understand that. Can you please rephrase?"}
