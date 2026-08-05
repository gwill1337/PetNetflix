import httpx2

payload1 = {
    "name": "FEAR",
    "title": "title for Fear",
    "image": "/FEAR.jpg",
    "rating": 8.0,
    "year": "2019"
}

payload2 = {
    "name": "Project Power",
    "title": "On the streets of New Orleans, word begins to spread about a mysterious new pill that unlocks superpower abilities unique to each user for five minutes. The catch? You don't know what will happen until you take it. To stop the epidemic, a teenage dealer, a local cop, and an ex-soldier with a secret vendetta must team up and take down the group responsible for creating it.",
    "image": "/project-power.jpg",
    "rating": 9.0,
    "year": "2023"
}

def post_movies():
    with httpx2.Client() as client:
        client.post("http://localhost:8000/movie", json=payload1)
        client.post("http://localhost:8000/movie", json=payload2)
        print("post ended")

def update_movies():
    with httpx2.Client() as client:
        client.put("http://localhost:8000/movie/3", json=payload1)
        client.put("http://localhost:8000/movie/4", json=payload2)
        print("updating ended")

# post_movies()
update_movies()