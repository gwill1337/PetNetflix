import { lazy, Suspense, useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import FavoriteButton from "./FavoriteButton";
import { useDebounce } from './hooks/useDebounce';
import { useTheme } from './hooks/useTheme';
import { SetHeader } from "./Header";
import { useAuth } from "./hooks/useAuth";
import { API_URL } from "./config";
const LazyMovieComments = lazy(() => import('./Comments'))

export function MovieDetails() {
    const { id } = useParams();
    const { userId, isLoggedIn, loading: authLoading } = useAuth();


    const [movie, setMovie] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (authLoading) return;

        const controller = new AbortController();

        async function fetchData() {
            setLoading(true);
            try {
                if (!isLoggedIn) {
                    const [movieRes, favoritesRes] = await Promise.all([
                        axios.get(`${API_URL}/movie/${id}`, { signal: controller.signal }),
                    ]);
                    setMovie(movieRes.data);
                    setIsFavorite(false);
                } else {
                    const [movieRes, favoritesRes] = await Promise.all([
                        axios.get(`${API_URL}/movie/${id}`, { signal: controller.signal }),
                        axios.get(`${API_URL}/favorites/${userId}`, { signal: controller.signal }),
                    ]);
                    setMovie(movieRes.data);
                    setIsFavorite(favoritesRes.data.includes(Number(id)));
                }
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
    }, [id, authLoading]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p className="text-red-500">Error: {error}</p>;
    if (!movie) return <p>Movie not found.</p>;

    return (
        <div className="w-full h-full bg-white dark:bg-black text-black dark:text-white px-6 py-5 flex flex-col">
            {/* <div className="fog-bg-red"/> */}
            {/* Movie details */}
            <div className="w-full flex items-start">
                {movie.image && (
                    <div className="relative shrink-0 w-md aspect-2/3">
                        <img
                            src={movie.image}
                            alt={movie.title || movie.name}
                            className="w-full h-full object-cover rounded-2xl shadow-lg"
                        />
                        <div className="absolute top-1 right-2 z-10">
                            <FavoriteButton
                                movieId={movie.movie_id}
                                userId={userId}
                                initialIsFavorite={isFavorite}
                            />
                        </div>
                    </div>
                )}
                <div className=" flex flex-col justify-between max-w-4xl py-2 p-6">
                    <p className="w-auto  text-base font-normal">{movie.description || movie.title}</p>
                    <div>
                        <p className="font-semibold text-amber-500">IMDb: {movie.rating}</p>
                        <p className="text-black/60 dark:text-white/60 text-sm">{movie.year}</p>
                    </div>
                </div>
            </div>
            <div className="w-full">
                <Suspense fallback={<p className="p-6">Loading comments...</p>}>
                    <LazyMovieComments movieId={movie.movie_id} />
                </Suspense>
            </div>
        </div>
    );
}