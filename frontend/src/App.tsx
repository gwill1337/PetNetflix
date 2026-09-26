import { useState, useEffect } from 'react';
import MovieCard from './components/MovieCard';
import axios from 'axios';
// import { useDebounce } from './hooks/useDebounce';
// import { useTheme } from './hooks/useTheme';
import { useAuth } from './hooks/useAuth';
import { API_URL } from './config/config';
import type { Movie } from './types/movie';

function App() {
  const { userId, isLoggedIn, loading: authLoading } = useAuth();

  // const [searchTerm, setSearchTerm] = useState<string>("");
  // const debouncedSearch = useDebounce(searchTerm, 400);

  const [movies, setMovies] = useState<Movie[]>([]);
  const [favoriteIds, setFavoriteIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (authLoading) return;

    const controller = new AbortController();

    async function fetchData() {
      setLoading(true);
      try {
        const moviesRes = await axios.get<Movie[]>(`${API_URL}/movies`, {
          signal: controller.signal,
        });
        setMovies(moviesRes.data);

        if (isLoggedIn && userId !== null) {
          const favoritesRes = await axios.get<number[]>(`${API_URL}/favorites`, {
            signal: controller.signal,
          });
          setFavoriteIds(new Set(favoritesRes.data));
        } else {
          setFavoriteIds(new Set());
        }
      } catch (err) {
        if (!axios.isCancel(err)) {
          const message = axios.isAxiosError(err)
            ? err.response?.data?.detail || err.message
            : "Something went wrong";
          setError(message);
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
        <main className='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-7 gap-6 justify-items-center max-w-[1800px] mx-auto'>
          {loading && <p>Loading, please wait. This may take 30-90 seconds.</p>}
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