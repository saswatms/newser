import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './NewsList.css';

function NewsList() {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(true); // Track loading state for feedback

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      const response = await axios.get('/get_news');
      setArticles(response.data);
    } catch (error) {
      console.error('Error fetching the news articles:', error);
    } finally {
      setIsLoading(false); // Set loading state to false after fetch (success or failure)
    }
  };

  const handleFetchNews = async () => {
    setIsLoading(true); // Set loading state before fetching
    try{
      const response = await axios.get('/fetch_news');
      await fetchArticles()
    }catch(error){
      console.log('Error')}
  };

  return (
    <div className="news-container">
      <header className="App-header">
        <h1>News Curator</h1>
        <button className="fetch-button" onClick={handleFetchNews}>
          Fetch News
        </button>
      </header>
      <div className="news-list-container">
        {isLoading ? (
          <div className="loading-indicator">
            <p>Fetching news articles...</p>
          </div>
        ) : (
          <ul className="news-list">
            {articles.map((article, index) => (
              <li key={index} className="news-item">
                <div className="news-item-content">
                  <a href={article.link} target="_blank" rel="noopener noreferrer">
                    {article.title}
                  </a>
                  <p>{article.summary}</p>
                  <small className="published-date">{article.published}</small>
                  <small className="source">{article.source}</small>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default NewsList;
