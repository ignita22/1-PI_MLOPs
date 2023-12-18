from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI()


@app.get('/PlayTimeGenre/{genre}')

def PlayTimeGenre(genre):
    
    genre_df = tabla[tabla['genres'].str.contains(genre, case=False, na=False)]

    max_playtime_year = genre_df.groupby('year')['playtime_forever'].sum().idxmax()

    return max_playtime_year



@app.get('/UserForGenre/{genre}')

def UserForGenre(genre):

    genre_data = tabla[tabla['genres'].str.contains(genre, case=False)]

    max_playtime_users = genre_data.groupby('genres').apply(lambda x: x.loc[x['playtime_forever'].idxmax()]['user_id']).reset_index(name='user_id')

    playtime_by_year = genre_data.groupby(['genres', 'year'])['playtime_forever'].sum().reset_index()

    return max_playtime_users, playtime_by_year


