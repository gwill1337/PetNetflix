import { createContext } from "react"

export type ThemeContextType = "light" | "dark";

export interface IThemeContextType {
    theme: ThemeContextType;
    toggleTheme: () => void;
}

export const ThemeContext = createContext<IThemeContextType | undefined>(undefined);