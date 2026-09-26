<!-- # PetNetflix
## About
PetNetflix this is a project thats was made for practional and demonstational purposes.   
PetNetflix includes — Auth, OAuth 2.0/OpenID via Google, comments section, favorite buttons.


## Arhitecture
### Backend:
Backend uses FastAPI for REST API and PostgreSQL for stored films, comments, users, and refresh tokens.

### Frontend:
Fronted uses react, vite, and tailwindcss v4.0 for css.


## Deployment
*For deployments section we take that all infra uses free tier subscription.*
* **Backend:** Deployed on Render.
* **DataBase:** Deployed on Neon.tech.
* **Frontend:** Deployed on Vercel.  -->

# PetNetflix

A Netflix-style movie browsing app built as a pet/portfolio project to practice full-stack development: authentication (including Google OAuth), favorites, comments, and search.

**🔗 Live demo:** [pet-netflix.vercel.app](https://pet-netflix.vercel.app/)

> ⚠️ Hosted on free-tier infrastructure — the backend may take **30–90 seconds** to wake up on the first request.

---

## About

PetNetflix is a small full-stack application made for practice and demonstration purposes. It lets users browse a movie catalog, search in real time, sign up/sign in (email+password or Google), mark movies as favorites, and leave comments on movie pages.

## Features

- **Authentication**
  - Email/password sign up & sign in
  - Google OAuth 2.0 / OpenID Connect login
  - JWT access tokens + rotating refresh tokens stored in `httpOnly` cookies
  - Silent session refresh on token expiry
- **Movies**
  - Browsable movie grid with poster, rating, and details page
  - Debounced live search
- **Favorites** — add/remove movies from your favorites (persisted per user)
- **Comments** — post and delete comments on a movie's page
- **UI**
  - Light/dark theme with persisted preference
  - Responsive grid layout

## Architecture

### Backend
- **FastAPI** — async REST API
- **PostgreSQL** — stores movies, users, comments, favorites, and sessions
- **SQLAlchemy (async)** — ORM layer
- **Authlib** — Google OAuth 2.0 / OpenID Connect flow
- **PyJWT + bcrypt** — token issuance and password hashing
- Access token + hashed refresh token (rotated on each refresh) stored server-side per session, both delivered as secure `httpOnly` cookies

### Frontend
- **React + TypeScript**
- **Vite** — build tooling
- **Tailwind CSS v4** — styling
- **React Router** — routing
- **Axios** — API calls with `withCredentials` for cookie-based auth

## Deployment

All infrastructure runs on free-tier plans:

| Layer      | Provider     |
|------------|--------------|
| Frontend   | [Vercel](https://vercel.com/)      |
| Backend    | [Render](https://render.com/)      |
| Database   | [Neon.tech](https://neon.tech/)    |

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (e.g. a free Neon project)
- Google OAuth credentials (Client ID/Secret) if you want to test Google login

### Backend

```bash
git clone https://github.com/gwill1337/PetNetflix.git
cd pet-netflix/backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the backend root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
JWT_KEY=your-secret-key
JWT_ALGORITHM=HS256
CORS=["http://localhost:5173"]
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
FRONTEND_URL=http://localhost:5173
```

Run the API:

```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd pet-netflix/frontend
npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

Run the dev server:

```bash
npm run dev
```

## Main API Endpoints

| Method | Endpoint                  | Description                     |
|--------|---------------------------|----------------------------------|
| POST   | `/auth/register`          | Create a new account             |
| POST   | `/auth/login`             | Log in with email/password       |
| GET    | `/auth/google/login`      | Start Google OAuth flow          |
| POST   | `/auth/refresh`           | Rotate/refresh session tokens    |
| POST   | `/auth/logout`            | Log out and revoke session       |
| GET    | `/me`                     | Get the current logged-in user   |
| GET    | `/movies`                 | List all movies                  |
| GET    | `/movie/{movie_id}`       | Get movie details                |
| GET    | `/search/movie`           | Search movies by name            |
| GET    | `/favorites`              | Get current user's favorites     |
| POST   | `/favorite`               | Add a movie to favorites         |
| DELETE | `/favorite`               | Remove a movie from favorites    |
| GET    | `/comments/{movie_id}`    | Get comments for a movie         |
| POST   | `/comments`               | Post a comment                   |
| DELETE | `/comments`               | Delete your own comment          |

## Tech Stack Summary

**Frontend:** React · TypeScript · Vite · Tailwind CSS v4 · React Router · Axios
**Backend:** FastAPI · SQLAlchemy (async) · PostgreSQL · Authlib · PyJWT · bcrypt

---

Made as a pet project to practice full-stack development with authentication flows.