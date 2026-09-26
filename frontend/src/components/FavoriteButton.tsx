import { memo, useEffect, useState } from "react";
import axios, { isAxiosError } from 'axios';
import { API_URL } from "../config/config";

interface FavoriteButtonType {
    movieId: number;
    userId: number;
    initialIsFavorite: boolean;
}

function FavoriteButton({ movieId, userId, initialIsFavorite = false }: FavoriteButtonType) {
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
                await axios.post(`${API_URL}/favorite/${userId}`, payload);
            } else
                await axios.delete(`${API_URL}/favorite/${userId}`, { data: payload });
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