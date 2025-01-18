Getting Started
Prerequisites
Ensure that you have the following installed:

Python 3.7+
Node.js
npm or yarn
Git
Backend Setup (FastAPI)
Install the required Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt

Run the backend server:

bash
Copy
Edit
uvicorn main:app --reload

Navigate to the frontend directory:

bash
Copy
Edit
cd frontend
Install the required Node.js dependencies:

bash
Copy
Edit
npm install
or if you're using yarn:

bash
Copy
Edit
yarn install
Run the development server:

bash
Copy
Edit
npm run dev
The frontend will now be running at http://localhost:3000.

API Endpoints
POST /recommend
This endpoint recommends songs based on a song ID.

Request Body:

json
Copy
Edit
{
  "song_id": 1
}
Response:

json
Copy
Edit
{
  "recommendations": ["Song A", "Song C", "Song D"]
}
POST /chatbot
This endpoint handles chatbot queries.

Request Body:

json
Copy
Edit
{
  "query": "What is your name?"
}
Response:

json
Copy
Edit
{
  "response": "I am MusicBot! How can I help you?"
}
