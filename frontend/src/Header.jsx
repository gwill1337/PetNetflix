import { useEffect, useRef, useState } from "react";
import { useTheme } from "./hooks/useTheme";
import { useDebounce } from "./hooks/useDebounce";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthModal } from "./AuthModal";

export function SetHeader() {
    const { theme, toggleTheme } = useTheme();
    const [searchTerm, setSearchTerm] = useState("");
    const debouncedSearch = useDebounce(searchTerm, 400);
    const [results, setResults] = useState([]);
    const [open, setOpen] = useState(false);
    const boxRef = useRef(null);
    const navigate = useNavigate();

    const [authOpen, setAuthOpen] = useState(false);

    const API_URL = "http://localhost:8000";

    useEffect(() => {
        if (!debouncedSearch.trim()) {
            setResults([]);
            setOpen(false);
            return;
        }
        const controller = new AbortController();
        axios
            .get(`${API_URL}/search/movie`, {
                params: { movie_name: debouncedSearch },
                signal: controller.signal,
            })
            .then((res) => {
                setResults(res.data);
                setOpen(true);
            })
            .catch((err) => {
                if (!axios.isCancel(err)) console.error(err);
            });
        return () => controller.abort();
    }, [debouncedSearch]);

    useEffect(() => {
        function handleClick(e) {
            if (boxRef.current && !boxRef.current.contains(e.target)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);

    function handleSelect(movieId) {
        setOpen(false);
        setSearchTerm("");
        navigate(`/movie/${movieId}`);
    }

    return (
        <header className='mb-10 flex items-center justify-between'>
            <Link to="/">
                <img
                    src="/Logonetflix.png"
                    alt="Netflix"
                    className='h-8 w-auto'
                />
            </Link>

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
                <button
                    onClick={() => setAuthOpen(true)}
                    className='text-sm px-3 py-1 outline-0 font-semibold hover:bg-black/15 dark:hover:bg-white/15 transition rounded border border-black/20 dark:border-white/20 cursor-pointer h-9'
                >
                    Sign In
                </button>

                <AuthModal
                    isOpen={authOpen}
                    onClose={() => setAuthOpen(false)}
                    onAuthSuccess={(user) => console.log("Успешный вход:", user)}
                />

                {open && results.length > 0 && (

                    <div className="absolute top-11 right-0 w-72 max-h-96 overflow-y-auto bg-white dark:bg-neutral-900 border border-black/15 dark:border-white/15 rounded-lg shadow-xl z-50">
                        {results.map((movie) => (
                            <div
                                key={movie.movie_id}
                                onClick={() => handleSelect(movie.movie_id)}
                                className="flex items-center gap-2 p-2 hover:bg-black/5 dark:hover:bg-white/10 cursor-pointer"
                            >
                                <img src={movie.image} alt="" className="w-8 h-11 object-cover rounded" />
                                <span className="text-sm"> {movie.name}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </header>
    );
}