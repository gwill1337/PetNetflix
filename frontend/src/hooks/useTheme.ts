import { useContext } from "react"
import { ThemeContext } from "../context/theme.context"
import type { IThemeContextType } from "../context/theme.context"

export function useTheme(): IThemeContextType {
    const ctx = useContext(ThemeContext)
    if (!ctx) {
        throw new Error("useTheme must be used within ThemeProvider")
    }
    return ctx
}