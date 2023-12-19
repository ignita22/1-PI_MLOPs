from fastapi import FastAPI
import pandas as pd
import numpy as np


# cargamos los datos
user_reviews_final = pd.read_csv('datasets/df_user_reviews_final.csv',low_memory=False)
user_items_explode = pd.read_csv('datasets/df_user_items_explode.csv',low_memory=False)
steam_games_clean= pd.read_csv('datasets/df_steam_games_clean.csv',low_memory=False)
tabla = pd.read_csv("datasets/tabla.csv", sep=",")


app = FastAPI()


@app.get('/PlayTimeGenre/{genre}')

def PlayTimeGenre(genre: str):
    # Filtrar por el género especificado
    sample_size = 10000  # Definir el tamaño de la muestra
    total_rows = tabla.shape[0]

    if total_rows > sample_size:
        random_indices = random.sample(range(total_rows), sample_size)
        genre_df = tabla.loc[random_indices]
    else:
        genre_df = tabla

    genre_df = genre_df[genre_df['genres'].str.contains(genre, case=False, na=False)]

    max_playtime_year = genre_df.groupby('year')['playtime_forever'].sum().idxmax()

    return max_playtime_year



@app.get('/UserForGenre/{genre}')

def UserForGenre(genre):

    genre_data = tabla[tabla['genres'].str.contains(genre, case=False)]

    max_playtime_users = genre_data.groupby('genres').apply(lambda x: x.loc[x['playtime_forever'].idxmax()]['user_id']).reset_index(name='user_id')

    playtime_by_year = genre_data.groupby(['genres', 'year'])['playtime_forever'].sum().reset_index()

    return max_playtime_users, playtime_by_year


