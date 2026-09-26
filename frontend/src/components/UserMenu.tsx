import { useEffect, useRef, useState } from "react";

export interface UserMenuType {
    username?: string;
    email?: string;
    onLogout: () => void;
}

export function UserMenu({ username, email, onLogout }: UserMenuType) {
    const [open, setOpen] = useState(false);
    const boxRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        function handleClick(e: MouseEvent) {
            const target = e.target;
            if (boxRef.current && target instanceof Node && !boxRef.current.contains(target)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);


    function handleLogoutClick() {
        setOpen(false);
        onLogout?.();
    }


    return (
        <div className="relative" ref={boxRef}>
            <button
                onClick={() => setOpen((prev) => !prev)}
                className="w-9 h-9 rounded-full bg-black/15 dark:bg-white/15 flex items-center justify-center font-semibold cursor-pointer"
            >
                {username?.[0]?.toUpperCase() || "U"}
            </button>

            {open && (
                <div className="absolute top-11 right-0 w-56 bg-white dark:bg-neutral-900 border border-black/15 dark:border-white/15 rounded-lg shadow-xl z-50 p-3">
                    <p className="font-semibold text-sm truncate">{username}</p>
                    <p className="text-black/60 dark:text-white/60 text-xs truncate mb-3">{email}</p>
                    <button
                        onClick={handleLogoutClick}
                        className="w-full text-sm px-3 py-2 rounded bg-black text-white dark:bg-white dark:text-black font-semibold hover:opacity-90 transition cursor-pointer"
                    >
                        Log out
                    </button>
                </div>
            )}
        </div>
    );

}