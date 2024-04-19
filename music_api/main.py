import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.metrics import pairwise_distances


# Exemple de données pour les chansons
data = {
    "Song1": [0.1, 0.2, 0.4],
    "Song2": [0.1, 0.25, 0.5],
    "Song3": [0.2, 0.1, 0.4],
    "Song4": [0.3, 0.4, 0.5],
    "Song5": [0.25, 0.35, 0.45],
    "Song6": [0.4, 0.4, 0.4],
}
df_songs = pd.DataFrame(data).T
df_songs.columns = ["Feature1", "Feature2", "Feature3"]

# Base de données pour les utilisateurs
df_users = pd.DataFrame(columns=["first_name", "last_name", "age"])
user_registered = False  # Indicateur d'enregistrement de l'utilisateur

app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str
    age: int


@app.get("/healthcheck/")
async def healthcheck():
    return {"body": "Server is running"}


@app.post("/register/")
async def register_user(user: User):
    global df_users, user_registered
    # Ajouter l'utilisateur à la DataFrame
    df_users = df_users.append(
        {"first_name": user.first_name, "last_name": user.last_name,
         "age": user.age},
        ignore_index=True,
    )
    user_registered = True  # Mettre à jour le statut d'enregistrement
    return {"message": "User registered successfully"}


@app.get("/songs/{song_name}")
async def get_similar_songs(song_name: str):
    if not user_registered:
        raise HTTPException(status_code=403, detail="User not registered")

    if song_name not in df_songs.index:
        raise HTTPException(status_code=404, detail="Song not found")

    # Calculer la distance entre la chanson sélectionnée et toutes les autres
    distances = pairwise_distances(
        df_songs.loc[[song_name]], df_songs, metric="euclidean"
    )[0]
    distance_series = pd.Series(distances, index=df_songs.index)
    sorted_distances = distance_series.sort_values()

    # Retourner les 5 chansons les plus proches
    closest_songs = sorted_distances[1:6].index.tolist()
    # Exclure la chanson elle-même
    return {"song_name": song_name, "closest_songs": closest_songs}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
