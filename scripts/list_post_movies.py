import httpx2
from pathlib import Path

def read_description(filename: str) -> str:
    return Path("descriptions", filename).read_text(encoding="utf-8")


payload1 = {
    "name": "FEAR",
    "title": "title for Fear",
    "description": read_description("fear.txt"),
    "image": "/FEAR.jpg",
    "rating": 8.3,
    "year": "2019"
}


payload2 = {
    "name": "Project Power",
    "title": "title for Project Power",
    "description": read_description("project_power.txt"),
    "image": "/project-power.jpg",
    "rating": 9.0,
    "year": "2023"
}

payload3 = {
    "name": "Breaking Bad",
    "title": "Breaking Bad",
    "description": "Breaking bad description",
    "image": "/BreakingBad.jpg",
    "rating": 9.9,
    "year": "2008"
}

def post_movies():
    with httpx2.Client() as client:
        client.post("http://localhost:8000/movie", json=payload1)
        client.post("http://localhost:8000/movie", json=payload2)
        client.post("http://localhost:8000/movie", json=payload3)
        print("post ended")

def update_movies():
    with httpx2.Client() as client:
        client.put("http://localhost:8000/movie/3", json=payload1)
        client.put("http://localhost:8000/movie/4", json=payload2)
        print("updating ended")

post_movies()
# update_movies()