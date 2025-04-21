import React, { useState } from 'react';
import './App.css';

function App() {
  const [movieTitle, setMovieTitle] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const getRecommendations = async () => {
    if (!movieTitle) return;

    const response = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: movieTitle }),
    });
    const data = await response.json();
    if(!response.ok) {
      console.error('Error getting the recommendation:' + data.error);
    }
    setRecommendations(data);
  };
  return (
    <div className='container'>
      <h1>Movie Recommendation System</h1>
      <input
        id = 'search-bar'
        type="text"
        placeholder="Enter a movie title"
        value={movieTitle}
        onChange={(e) => setMovieTitle(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />
      <button id='button'onClick={getRecommendations} style={{ marginLeft: "10px", padding: "10px" }}>
        Get Movies
      </button>
      <h2>Top 5 Recommended Movies:</h2>
      <ul>
        {recommendations.map((movie, index) => (
          <li key={index}>{movie}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
