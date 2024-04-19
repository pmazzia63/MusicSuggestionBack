import os

import uuid
import boto3
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from music_api.utils import find_similar_songs


path_data = os.getcwd() + "/music_api/dataset.csv"

# Base de donnée pour les chansons
df_songs = pd.read_csv(path_data, index_col=0)

# Indicateur d'enregistrement de l'utilisateur
user_registered = False


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],  # Or specify methods ["GET", "POST", etc.]
    allow_headers=["*"],
)


class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str


class Song(BaseModel):
    artist: str
    track: str


@app.get("/healthcheck/")
async def healthcheck():
    return {"body": "Server is running"}


@app.post("/reset/")
async def reset():
    global user_registered
    user_registered = False  # Mettre à jour le statut d'enregistrement


@app.post("/register/")
async def register_user(user: User):
    global user_registered

    # Create an S3 client
    s3 = boto3.client('s3')

    # Specify the file to upload
    bucket_name = 'datauser'

    # Serialize user data to JSON
    user_data_json = user.model_dump_json()

    # Specify the filename and the bucket name
    filename = f'userdata_{uuid.uuid4()}.json'
    bucket_name = 'datauser'

    # Save user data to a file
    with open(filename, 'w') as file:
        file.write(user_data_json)

    # Upload the file
    try:
        s3.upload_file(filename, bucket_name, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    user_registered = True

    return {"message": "User data uploaded to S3 successfully"}


@app.post("/songs/")
async def get_similar_songs(song: Song):
    global user_registered, df_songs

    if not user_registered:
        raise HTTPException(status_code=403, detail="User not registered")

    result = find_similar_songs(df_songs, song.artist, song.track)
    print(result)
    return result.to_dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
