import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

import { useState, useEffect } from 'react';
import  MovieCard  from './MovieCard';
import  FavoriteButton from './FavoriteButton';
import "./index.css";
import axios from 'axios';
import { useDebounce } from './hooks/useDebounce';
import { useTheme } from './hooks/useTheme';


const API_URL = "http://localhost:8000";

function App() {

  const {theme, toggleTheme} = useTheme();
  
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 400);
  
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

    return () => controller.abort();
  }, [userId]);

  // useEffect(() => {
  //   const controller = new AbortController();
    
  //   async function fetchMovies() {
  //     setLoading(true);
  //     try {
  //       let res;
  //       if (debouncedSearch.trim()) {
  //         res = await axios.get(`${API_URL}/search/movie`, {
  //           params: {movie_name: debouncedSearch},
  //           signal: controller.signal
  //         });
  //       } else {
  //         res = await axios.get(`${API_URL}/movies`,{
  //           signal: controller.signal
  //         });
  //       }
  //       setMovies(res.data);
  //     } catch (err) {
  //       if (!axios.isCancel(err)) setError(err.message);
  //     } finally {
  //       setLoading(false);
  //     }
  //   }

  //   fetchMovies();
  //   return () => controller.abort();
  // }, [debouncedSearch]);
  
  return (
    <div className='min-h-screen w-full bg-white dark:bg-black text-black dark:text-white px-6 py-5'>
      {/* <header className='mb-10 flex items-center justify-between'>
        <img 
        src="/Logonetflix.png"
        alt="Netflix"
        className='h-8 w-auto'
        />
        
        <div className='flex items-center gap-1'>
        <input type="search" value={searchTerm} onChange={e => {
          setSearchTerm(e.target.value)
        }}
        placeholder="Search..."
        className='border border-black/15 dark:border-white/15 px-2 py-1 rounded outline-0 w-60 h-9'
        />
        <button
          onClick={toggleTheme}
          className='text-sm px-3 py-1 outline-0 font-semibold hover:bg-black/15 dark:hover:bg-white/15 transition rounded border border-black/20 dark:border-white/20 cursor-pointer h-9'
        >
          {theme === "dark" ? "☀ Light" : "🌙 Dark"}
        </button>
        </div>
      </header> */}
      <main className=' flex gap-6 '>
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
