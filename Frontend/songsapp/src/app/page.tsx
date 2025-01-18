import React from "react";
import RecommendationForm from "../components/RecommendationForm";

const Home: React.FC = () => {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>🎵 Song Recommendation App</h1>
      <RecommendationForm />
    </div>
  );
};

export default Home;
