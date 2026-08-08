import { useEffect, useState } from "react";
import { API_URL } from "./config";
import axios from "axios";
import { useAuth } from "./hooks/useAuth";



function Comments({ movieId }) {
    const { userId, isLoggedIn } = useAuth();

    const [comments, setComments] = useState([]);
    const [text, setText] = useState("");
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);

    useEffect(() => {
        const controller = new AbortController();

        axios
            .get(`${API_URL}/comments/${movieId}`, { signal: controller.signal })
            .then((res) => setComments(res.data))
            .catch((err) => {
                if (!axios.isCancel(err)) console.error(err);
            })
            .finally(() => setLoading(false));
        return () => controller.abort();
    }, [movieId])

    async function handleAdd(e) {
        e.preventDefault();
        if (!text.trim() || sending) return;

        setSending(true);
        try {
            const res = await axios.post(`${API_URL}/comments`, {
                movie_id: movieId,
                text: text.trim(),
            }, { withCredentials: true },
            );
            setComments((prev) => [res.data, ...prev]);
            setText("");
        } catch (err) {
            console.error(err);
        } finally {
            setSending(false);
        }
    }

    async function handleDelete(commentId) {
        const prev = comments;
        setComments((c) => c.filter((cm) => cm.id !== commentId));
        try {
            await axios.delete(`${API_URL}/comments`, {
                params: { comment_id: commentId, user_id: userId },
                withCredentials: true,
            });
        } catch (err) {
            console.error(err);
            setComments(prev);
        }
    }

    return (
        <div className="w-full max-w-4xl mt-8">
            <h3 className="text-lg font-bold mb-3">Comments</h3>

            {isLoggedIn && (
                <form onSubmit={handleAdd} className="flex gap-2 mb-4">
                    <input
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Write comment"
                        className="flex-1 border rounded border-black/15 dark:border-white/15 outline-0 px-2 h-10 bg-transparent"
                    />
                    <button
                        type="submit"
                        disabled={sending}
                        className="px-4 h-10 rounded bg-black text-white dark:bg-white dark:text-black cursor-pointer"
                    >
                        Post
                    </button>
                </form>
            )}

            {loading && <p className="text-black/60 dark:text-white/60 text-sm">Loading...</p>}

            {!loading && comments.length === 0 && (
                <p className="text-black/60 dark:text-white/60 text-sm">No comments yet. Post first comment</p>
            )}

            <div className="flex flex-col gap-2">
                {comments.map((c) => (
                    <div
                        key={c.id}
                        className="flex items-center justify-between border border-black/15 dark:border-white/15 rounded-lg p-3"
                    >
                        <div>
                            <p className="flex-col text-xs italic">{c.user_username}:</p>
                            <p className="text-base">{c.comment_text}</p>
                        </div>
                        {c.user_id == userId && (
                            <button
                                onClick={() => handleDelete(c.id)}
                                className="text-black/50 dark:text-white/50 hover:text-red-500 transition cursor-pointer text-sm ml-3 shrink-0">
                                Delete
                            </button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Comments;