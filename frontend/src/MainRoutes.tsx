import { BrowserRouter as Router, Routes, Route} from "react-router-dom"
import App from "./App"
import {MovieDetails} from "./pages/MovieDetails"
import { Layout } from "./components/Layout"

export function MainRoutes() {
    return <Router>
        <Routes>
            <Route element={<Layout/>}>
                <Route
                    path="/"
                    element={<App />}
                    />
            </Route>
            <Route element={<Layout/>}>
                <Route
                    path="/movie/:id"
                    element={<MovieDetails />}
                />
            </Route>
        </Routes>
    </Router>
}