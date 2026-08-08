import axios from "axios";
import { useEffect, useState, useRef } from "react";
import { API_URL } from "./config";

export function AuthModal({ isOpen, onClose, onAuthSuccess }) {
    const [mode, setMode] = useState("signin");

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const boxRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            setEmail("");
            setPassword("");
            setConfirmPassword("");
            setError(null);
            setMode("signin");
        }
    }, [isOpen]);

    useEffect(() => {
        if (!isOpen) return;
        function handleKeyDown(e) {
            if (e.key === "Escape") onClose();
        }
        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, [isOpen, onClose]);

    function handleBackdropClick(e) {
        if (boxRef.current && !boxRef.current.contains(e.target)) {
            onClose();
        }
    }

    async function HandleSubmit(e) {
        e.preventDefault();
        setError(null);

        if (mode === "signup" && password !== confirmPassword) {
            setError("username or password invalid");
            return;
        }

        setLoading(true);
        try {
            const endpoint = mode === "signin" ? "/auth/login" : "/auth/register";
            const res = await axios.post(`${API_URL}${endpoint}`, {
                username,
                email,
                password,
            }, { withCredentials: true });

            await onAuthSuccess?.();
            onClose();
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                err.response?.data?.message ||
                "Something went wrong, try again."
            );
        } finally {
            setLoading(false);
        }
    }

    if (!isOpen) return null;

    return (
        <div
            onMouseDown={handleBackdropClick}
            className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 backdrop-blur-sm"
        >
            <div
                ref={boxRef}
                className="w-full max-w-sm rounded-2xl border border-black/15 dark:border-white/15 bg-white dark:bg-neutral-900 text-black dark:text-white p-6 shadow-xl"
            >
                <div className="mb-6 flex rounded-lg border border-black/15 dark:border-white/15 overflow-hidden">
                    <button
                        type="button"
                        onClick={() => setMode("signin")}
                        className={`flex-1 py-2 text-sm font-semibold transition cursor-pointer ${mode === "signin"
                                ? "bg-black text-white dark:bg-white dark:text-black"
                                : "hover:bg-black/5 dark:hover:bg-white/10"
                            }`}

                    >
                        Sign In
                    </button>
                    <button
                        type="button"
                        onClick={() => setMode("signup")}
                        className={`flex-1 py-2 text-sm font-semibold transition cursor-pointer ${mode === "signup"
                                ? "bg-black text-white dark:bg-white dark:text-black"
                                : "hover:bg-black/5 dark:hover:bg-white/10"
                            }`}
                    >
                        Sign Up
                    </button>
                </div>

                <h2 className="mb-4 text-lg font-bold">
                    {mode === "signin" ? "Sign In" : "Create account"}
                </h2>

                <form onSubmit={HandleSubmit} className="flex flex-col gap-3">
                    <input
                        type="Username"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        className="border border-black/15 dark:border-white/15 px-3 py-2 rounded outline-0 h-10 bg-transparent"
                    />
                    <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        className="border border-black/15 dark:border-white/15 px-3 py-2 rounded outline-0 h-10 bg-transparent"
                    />
                    <input
                        type="password"
                        required
                        minLength={6}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        className="border border-black/15 dark:border-white/15 px-3 py-2 rounded outline-0 h-10 bg-transparent"
                    />
                    {mode === "signup" && (
                        <input
                            type="password"
                            required
                            minLength={6}
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Confirm password"
                            className="border border-black/15 dark:border-white/15 px-3 py-2 rounded outline-0 h-10 bg-transparent"
                        />
                    )}

                    {error && (
                        <p className="text-sm text-red-500">{error}</p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-2 h-10 rounded bg-black text-white dark:bg-white dark:text-black font-semibold hover:opacity-90 transition cursor-pointer disabled:opacity-50"
                    >
                        {loading
                            ? "Wait..."
                            : mode === "signin"
                                ? "Sign In"
                                : "Register"}
                    </button>
                </form>
            </div>
        </div>
    )
}