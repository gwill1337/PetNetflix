import { FcGoogle } from "react-icons/fc";
import { API_URL } from "../config/config";

export function GoogleSignInButton() {
    return (
        <a
            href={`${API_URL}/auth/google/login`}
            className="flex items-center justify-center gap-2 rounded px-3 h-10 font-semibold mt-2 bg-black text-white dark:bg-white dark:text-black hover:opacity-90 transition cursor-pointer disabled:opacity-50 w-full"
        >
            <FcGoogle className="w-5 h-5" />
            <span>Continue with Google</span>
        </a>
    )
}