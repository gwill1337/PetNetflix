import { FavoriteButton } from "./FavoriteButton";

export function MovieCard({image, movieId, userId, rating, isFavorite }) {
    return (
        <div className="relative w-50 rounded-2xl overflow-hidden shadow-lg">
            <img src={image}
            alt="Movie Poster"
            className="w-full h-auto object-cover"
            />
            <div className="absolute bottom-0 left-0 w-full bg-linear-to-t from-black/80 to-transparent p-2 text-sm text-white font-semibold">
                IMDb: {rating}
            </div>
            <div className="absolute top-2 right-2">
                <FavoriteButton movieId={movieId} userId={userId} initialIsFavorite={isFavorite} />
            </div>
        </div>
    )
}