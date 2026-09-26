import { useEffect, useState, useCallback, type PropsWithChildren } from "react";
import axios from "axios";
import { AuthContext, type AuthContextType } from "../context/auth.context";
import { API_URL } from "../config/config";



export function AuthProvider({ children }: PropsWithChildren) {
    const [user, setUser] = useState<AuthContextType["user"]>(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = useCallback(async () => {
        try {
            const res = await axios.get(`${API_URL}/me`, { withCredentials: true });
            setUser(res.data);
        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.status === 401) {
                try {
                    await axios.post(`${API_URL}/auth/refresh`, {}, { withCredentials: true });
                    const res = await axios.get(`${API_URL}/me`, { withCredentials: true });
                    setUser(res.data);
                } catch {
                    setUser(null);
                }
            } else {
                setUser(null);
            }
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUser();
    }, [fetchUser]);

    async function logout() {
        try {
            await axios.post(`${API_URL}/auth/logout`, {}, { withCredentials: true });
        } catch (err) {
            console.error(err);
        } finally {
            setUser(null);
        }
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                userId: user?.user_id ?? null,
                isLoggedIn: !!user,
                loading,
                setUser,
                logout,
                refetchUser: fetchUser,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}