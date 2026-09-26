import { lazy, Suspense, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import FavoriteButton from "../components/FavoriteButton";
// import { useDebounce } from '../hooks/useDebounce';
// import { useTheme } from '../hooks/useTheme';
// import { SetHeader } from "./Header";
import { useAuth } from "../hooks/useAuth";
import { API_URL } from "../config/config";
import type { MovieDetailsType } from "../types/movie";
const LazyMovieComments = lazy(() => import('../components/Comments'))

export function MovieDetails() {
    const { id } = useParams<{ id: string }>();
    const { userId, isLoggedIn, loading: authLoading } = useAuth();


    const [movie, setMovie] = useState<MovieDetailsType | null>(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (authLoading) return;

        const controller = new AbortController();

        async function fetchData() {
            setLoading(true);
            try {
                const movieRes = await axios.get(`${API_URL}/movie/${id}`, { signal: controller.signal });
                setMovie(movieRes.data);

                if (!isLoggedIn || userId === null) {
                    setIsFavorite(false);
                    return;
                }

                const favoritesRes = await axios.get(`${API_URL}/favorites`, { signal: controller.signal });
                setIsFavorite(favoritesRes.data.includes(Number(id)));
            } catch (err: unknown) {
                if (!axios.isCancel(err)) {
                    const message = err instanceof Error ? err.message : "Unknown error";
                    setError(message);
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
                        {isLoggedIn && (
                            <div className="absolute top-1 right-2 z-10">
                                <FavoriteButton
                                    movieId={movie.movie_id}
                                    initialIsFavorite={isFavorite}
                                />
                            </div>
                        )}
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