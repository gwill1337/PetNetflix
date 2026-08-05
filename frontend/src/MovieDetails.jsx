import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import FavoriteButton from "./FavoriteButton";
import { useDebounce } from './hooks/useDebounce';
import { useTheme } from './hooks/useTheme';
import { SetHeader } from "./Header";

const API_URL = "http://localhost:8000";

export function MovieDetails() {
    const { id } = useParams();
    const userId = 1;

    const [movie, setMovie] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();

        async function fetchData() {
            setLoading(true);
            try {
                const [movieRes, favoritesRes] = await Promise.all([
                    axios.get(`${API_URL}/movie/${id}`, { signal: controller.signal }),
                    axios.get(`${API_URL}/favorites?user_id=${userId}`, { signal: controller.signal }),
                ]);

                setMovie(movieRes.data);
                setIsFavorite(favoritesRes.data.includes(Number(id)));
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
    }, [id]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p className="text-red-500">Error: {error}</p>;
    if (!movie) return <p>Movie not found.</p>;

    return (
        <div className="w-1/2 h-full bg-white dark:bg-black text-black dark:text-white px-6 py-5 flex">
            {/* Movie details */}
                {movie.image && (
                    <div className="relative shrink-0 max-w-7/12 max-h-512">
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
                <div className="flex-1 flex flex-col justify-between py-2 p-6">
                    <h1 className="w-96 text-xl font-bold">{movie.title || movie.name}</h1>
                    <div>
                        <p className="font-semibold text-amber-500">IMDb: {movie.rating}</p>
                        <p className="text-black/60 dark:text-white/60 text-sm">{movie.year}</p>
                    </div>
                </div>
        </div>
    );
}