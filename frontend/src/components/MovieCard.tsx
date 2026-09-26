import { Link } from "react-router-dom";
import FavoriteButton from "./FavoriteButton";
import { memo } from "react";
import type { movieCard } from "../types/movie";
import { useAuth } from "../hooks/useAuth";



function MovieCard({ image, movieId, rating, isFavorite }: movieCard) {
    const { isLoggedIn } = useAuth();
    return (
        <div className="relative w-full  aspect-2/3 rounded-2xl overflow-hidden shadow-lg">
            <Link to={`movie/${movieId}`} className="block w-full h-full">
                <img src={image}
                    alt="Movie Poster"
                    className="w-full h-auto object-cover"
                />
            </Link>
            <div className="absolute bottom-0 left-0 w-full bg-linear-to-t from-black/80 to-transparent p-2 text-sm text-white font-semibold">
                IMDb: {rating}
            </div>
            <div className="absolute top-2 right-2">
                {isLoggedIn && (
                    <FavoriteButton movieId={movieId} initialIsFavorite={isFavorite} />
                )}
            </div>
        </div>
    )
}

export default memo(MovieCard)