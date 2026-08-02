import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

import { useState, useEffect } from 'react';
import { MovieCard } from './MovieCard';
import { FavoriteButton } from './FavoriteButton';
import "./App.css";
import axios from 'axios';

const API_URL = "http://localhost:8000";

function App() {
  const [searchTerm, setSearchTerm] = useState("")
  
  const [movies, setMovies] = useState([]);
  const [favoriteIds, setFavoritesIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const userId = 1;

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        const [moviesRes, favoritesRes] = await Promise.all([
          axios.get(`${API_URL}/movies`, { signal: controller.signal}),
          axios.get(`${API_URL}/favorites?user_id=${userId}`, {signal: controller.signal})
        ]);

        // const moviesData = await moviesRes.json();
        // const favoritesData = await favoritesRes.json();

        setMovies(moviesRes.data)
        setFavoritesIds(new Set(favoritesRes.data));
      } catch (err) {
        if (!axios.isCancel(err)) {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    
    // async function fetchMovies() {
    //   try {
    //     const res = await fetch(`${API_URL}/movies`, {
    //       signal: controller.signal,
          
    //     });

    //     const data = await res.json();
    //     setMovies(data); 

    //   } catch (err) {
    //     if (err.name !== 'AbortError') {
    //       setError(err.message);
    //     }
    //   } finally {
    //     setLoading(false);
    //   }
    // }

    // fetchMovies();

    return () => controller.abort();
  }, [userId]);
  
  return (
    <div className='min-h-screen w-full bg-black text-white px-6 py-5'>
      <header className='mb-10 flex items-center'>
        <img 
        src="/Logonetflix.png"
        alt="Netflix"
        className='h-8 w-auto'
        />

        <input type="search" />
      </header>
      <main className=' flex gap-6'>
        {loading && <p>Loading...</p>}
        {error && <p className='text-red-500'>Error: {error}</p>}
        {!loading && !error && movies.map((movie) => (
          <MovieCard
          key={movie.movie_id}
          movieId={movie.movie_id}
          userId={userId}
          image={movie.image}
          rating={movie.rating}
          isFavorite={favoriteIds.has(movie.movie_id)}
          />
        ))}
      </main>
    </div>
  )
}

export default App;
