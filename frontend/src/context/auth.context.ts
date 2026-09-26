import React, { createContext } from "react";

export interface AuthContextType {
    user: {user_id: number; username: string; email: string} | null;
    userId: number | null;
    isLoggedIn: boolean;
    loading: boolean;
    setUser: React.Dispatch<React.SetStateAction<AuthContextType["user"]>>;
    logout: () => Promise<void>;
    refetchUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);