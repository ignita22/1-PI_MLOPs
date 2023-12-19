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
    genre_df = tabla[tabla['genres'].str.contains(genre, case=False, na=False)].head(10000)

    # Encontrar el año con más horas jugadas para ese género
    max_playtime_year = genre_df.groupby('year')['playtime_forever'].sum().idxmax()

    return json.dumps({'genre': genre, 'max_playtime_year': int(max_playtime_year)})
    except Exception as e:
        return {'error': str(e), 'traceback': traceback.format_exc()}



@app.get('/UserForGenre/{genre}')

def UserForGenre(genre):

    genre_data = tabla[tabla['genres'].str.contains(genre, case=False)]

    max_playtime_users = genre_data.groupby('genres').apply(lambda x: x.loc[x['playtime_forever'].idxmax()]['user_id']).reset_index(name='user_id')

    playtime_by_year = genre_data.groupby(['genres', 'year'])['playtime_forever'].sum().reset_index()

    return max_playtime_users, playtime_by_year


