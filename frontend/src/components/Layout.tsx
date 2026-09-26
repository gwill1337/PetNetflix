import { Outlet } from "react-router-dom";
import { SetHeader } from "./Header";

export function Layout() {
    return (
        <div className="min-h-screen w-full bg-white dark:bg-black text-black dark:text-white px-6 py-5">
            <SetHeader/>
            <Outlet/>
        </div>
    );
}