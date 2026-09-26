import { useEffect, useState, type PropsWithChildren } from "react";
import { ThemeContext, type ThemeContextType } from "../context/theme.context";

export function ThemeProvider({children}: PropsWithChildren) {
    const [theme, setTheme] = useState<ThemeContextType>(() => {
        const storedTheme = localStorage.getItem("theme");
        return storedTheme === "light" || storedTheme === "dark" ? storedTheme : "dark";
    });

    useEffect (() => {
        document.documentElement.classList.toggle("dark", theme === "dark");
        localStorage.setItem("theme", theme);
    }, [theme]);

    const toggleTheme = () => setTheme(prev => (prev === "dark" ? "light" : "dark"))

    return (
        <ThemeContext.Provider
            value={{
                theme,
                toggleTheme
            }}
            >
            {children}
        </ThemeContext.Provider>
    )
}