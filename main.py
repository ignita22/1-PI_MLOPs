from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np


# cargamos los datos
user_reviews_final = pd.read_csv('datasets/df_user_reviews_final.csv',low_memory=False)
user_items_explode = pd.read_csv('datasets/df_user_items_explode.csv',low_memory=False)
steam_games_clean= pd.read_csv('datasets/df_steam_games_clean.csv',low_memory=False)
tabla = pd.read_csv("datasets/tabla.csv", sep=",")
recomendacion_juego = pd.read_csv('datasets/df_recomendacion_juego.csv',low_memory=False)


app = FastAPI()


@app.get('/PlayTimeGenre/{genre}')

async def PlayTimeGenre(genre: str):
    try: 
        # Filtrar por el género especificado
        genre_df = tabla[tabla['genres'].str.contains(genre, case=False, na=False)].head(10000)
    
        # Encontrar el año con más horas jugadas para ese género
        max_playtime_year = genre_df.groupby('year')['playtime_forever'].sum().idxmax()
    
        return {'genre': genre, 'max_playtime_year': int(max_playtime_year)}
    except Exception as e:
        return {'error': str(e), 'traceback': traceback.format_exc()}



@app.get('/UserForGenre/{genre}')

async def UserForGenre(genre: str):
    try:
        # Filtrar por el género específico en el DataFrame tabla
        df_genero = tabla[tabla['genres'].apply(lambda x: genre in x)]
        df_usuario = user_items_explode[user_items_explode['item_name'].str.contains(genre, case=False)]

        if df_genero.empty or df_usuario.empty:
            # Si alguno de los DataFrames está vacío, lanzar un error ValueError
            raise ValueError("No hay juegos o usuarios en el género especificado")

        # Encontrar el usuario con más horas jugadas para el género específico
        usuario_mas_horas = str(df_usuario.loc[df_usuario['playtime_forever'].idxmax()]['user_id'])

        # Obtener el total de horas jugadas por el usuario en ese género
        horas_mas_usuario = str(df_usuario['playtime_forever'].max())

        # Calcular la acumulación de horas jugadas por año para ese género
        acumulacion_horas_por_año = df_genero.groupby('year')['playtime_forever'].sum().reset_index()
        lista_acumulacion = [{"Año": int(año), "Horas": horas} for año, horas in zip(
            acumulacion_horas_por_año['year'], acumulacion_horas_por_año['playtime_forever'])]

        # Crear el diccionario de retorno con la información recopilada
        resultado = {
            "Usuario con más horas jugadas para Género " + genre: usuario_mas_horas,
            "Total de horas jugadas por el usuario": horas_mas_usuario,
            "Acumulación de horas jugadas por año": lista_acumulacion}

        return resultado  # Devolver el diccionario con la información solicitada
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")


@app.get('/UserRecommend/{year}')

async def UsersRecommend(year: int):
    try: 
        # Convertir la columna 'fecha' a datetime si no está en ese formato
        user_reviews_final['fecha'] = pd.to_datetime(user_reviews_final['fecha'], errors='coerce')
    
        # Filtrar por el año especificado
        df_specific_year = user_reviews_final[user_reviews_final['fecha'].dt.year == year]
    
        # Filtrar por recomendaciones positivas
        df_recomendados = df_specific_year[df_specific_year['recommend'] == True]
    
        # Obtener los tres juegos más recomendados
        df_recomendados_merged = df_recomendados.merge(user_items_explode[['item_id', 'item_name']], on='item_id', how='inner')
        top3_games = df_recomendados_merged['item_name'].value_counts().head(3)
    
        # Convertir el resultado a un formato de lista de diccionarios
        resultado = [{'Puesto ' + str(i + 1): juego} for i, juego in enumerate(top3_games.index)]
    
        return resultado

    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

@app.get('/UserNotRecommend/{year}') 

async def UsersNotRecommend(year: int):
    try:
        # Convertir la columna 'fecha' a datetime si no está en ese formato
        user_reviews_final['fecha'] = pd.to_datetime(user_reviews_final['fecha'], errors='coerce')
    
        # Filtrar por el año especificado
        df_specific_year = user_reviews_final[user_reviews_final['fecha'].dt.year == year]
    
        # Filtrar por recomendaciones negativas
        df_no_recomendados = df_specific_year[df_specific_year['recommend'] == False]
    
        # Obtener los tres juegos menos recomendados
        df_no_recomendados_merged = df_no_recomendados.merge(user_items_explode[['item_id', 'item_name']], on='item_id', how='inner')
        bottom3_games = df_no_recomendados_merged['item_name'].value_counts().head(3)
    
        # Convertir el resultado a un formato de lista de diccionarios
        resultado = [{'Puesto ' + str(i + 1): juego} for i, juego in enumerate(bottom3_games.index)]
    
        return resultado

    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")    


@app.get('/Sentiment_analysis/{year}')

async def Sentiment_analysis(year: int):
    try:

        # Convertir la columna 'fecha' a datetime si no está en ese formato
        user_reviews_final['fecha'] = pd.to_datetime(user_reviews_final['fecha'], errors='coerce')
    
        # Filtrar por el año especificado
        df_year = user_reviews_final[user_reviews_final['fecha'].dt.year == year]
    
        if df_year.empty:
            return {"error": "No hay datos para el año proporcionado"}
    
        # Contar la cantidad de registros por análisis de sentimiento
        sentiment_counts = df_year['sentiment_analysis'].value_counts().reset_index()
        sentiment_counts.rename(columns={'index': 'sentiment_analysis', 'sentiment_analysis': 'sentiment_analysis'}, inplace=True)
    
        # Convertir el DataFrame a un diccionario
        result = sentiment_counts.to_dict()
    
        return result

    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")    
  

@app.get('/recomendacion_juego/{item_id: str}')

async def recomendacion_juego(item_id: str):
    try:
        # Obtenemos la columna correspondiente para cada id
        columna_juego = recomendacion_juego[item_id]
        
        # Obtener los juegos con los mejores puntajes (menores que 1)
        games = columna_juego[columna_juego < 1.0].sort_values(ascending=False).head(5).index.tolist()
    
        return games
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")
