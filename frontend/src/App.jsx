import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

import { useState, useEffect } from 'react';
import MovieCard from './MovieCard';
import FavoriteButton from './FavoriteButton';
import "./index.css";
import axios from 'axios';
import { useDebounce } from './hooks/useDebounce';
import { useTheme } from './hooks/useTheme';
import { useAuth } from './hooks/useAuth';
import { API_URL } from "./config";

function App() {
  const { userId, isLoggedIn, loading: authLoading } = useAuth();

  const { theme, toggleTheme } = useTheme();

  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 400);

  const [movies, setMovies] = useState([]);
  const [favoriteIds, setFavoritesIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authLoading) return;

    const controller = new AbortController();

    async function fetchData() {
      try {
        const requests = [axios.get(`${API_URL}/movies`, { signal: controller.signal })];

        if (isLoggedIn) {
          requests.push(
            axios.get(`${API_URL}/favorites/${userId}`, { signal: controller.signal })
          );
        }

        const [moviesRes, favoritesRes] = await Promise.all(requests);

        setMovies(moviesRes.data)
        setFavoritesIds(new Set(favoritesRes ? favoritesRes.data : []));
      } catch (err) {
        if (!axios.isCancel(err)) {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();

    return () => controller.abort();
  }, [userId, isLoggedIn, authLoading]);

  return (
    <div className='min-h-screen w-full bg-white dark:bg-black text-black dark:text-white px-6 py-5'>
      <div className='relative'>

        <main className='flex gap-6'>
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
    </div>
  )
}

export default App;
