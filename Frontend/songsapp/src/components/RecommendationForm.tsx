"use client";

import React, { useState } from "react";

interface RecommendationResponse {
  recommendations: string[];
}

const RecommendationForm: React.FC = () => {
  const [songId, setSongId] = useState<number>(1);
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = async () => {
    setError(null); // Clear previous errors
    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ song_id: songId }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error: ${response.status} - ${errorText}`);
      }

      const data: RecommendationResponse = await response.json();
      setRecommendations(data.recommendations);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", textAlign: "center" }}>
      <label style={{ display: "block", marginBottom: "10px" }}>
        Enter Song ID:
      </label>
      <input
        type="number"
        value={songId}
        onChange={(e) => setSongId(Number(e.target.value))}
        style={{
          padding: "8px",
          width: "100%",
          marginBottom: "10px",
          border: "1px solid #ccc",
          borderRadius: "4px",
        }}
      />
      <button
        onClick={fetchRecommendations}
        style={{
          padding: "10px 20px",
          backgroundColor: "#0070f3",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Get Recommendations
      </button>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      {recommendations.length > 0 && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Recommendations:</h3>
          <ul>
            {recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RecommendationForm;
