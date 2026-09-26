import { memo, useEffect, useState } from "react";
import axios, { isAxiosError } from 'axios';
import { API_URL } from "../config/config";

interface FavoriteButtonType {
    movieId: number;
    initialIsFavorite: boolean;
}

function FavoriteButton({ movieId, initialIsFavorite = false }: FavoriteButtonType) {
    const [isFavorite, setIsFavorite] = useState(initialIsFavorite);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setIsFavorite(initialIsFavorite);
    }, [initialIsFavorite]);


    async function handleClick() {
        if (loading) return;

        const nextValue = !isFavorite;
        setIsFavorite(nextValue);
        setLoading(true);

        const payload = {
            movie_id: movieId,
        };

        try {
            if (!isFavorite) {
                await axios.post(`${API_URL}/favorite`, payload, { withCredentials: true});
            } else
                await axios.delete(`${API_URL}/favorite`, { data: payload, withCredentials: true });
        } catch (err) {
            setIsFavorite(!nextValue);
            const message = isAxiosError(err) ? err.response?.data?.message || err.message : undefined;
            console.error(message);
        } finally {
            setLoading(false);
        }
    }

    return <button onClick={handleClick} disabled={loading}>
        {isFavorite ? '💖' : '🖤'}
    </button>
}

export default memo(FavoriteButton)