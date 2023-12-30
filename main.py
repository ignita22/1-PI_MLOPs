from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np


# cargamos los datos
user_reviews_final = pd.read_csv('datasets/df_user_reviews_final.csv',low_memory=False)
user_items_explode = pd.read_csv('datasets/df_user_items_explode.csv',low_memory=False)
steam_games_clean= pd.read_csv('datasets/df_steam_games_clean.csv',low_memory=False)
tabla = pd.read_csv("datasets/tabla.csv", sep=",")
simil_coseno = pd.read_csv('datasets/df_simil_coseno.csv',low_memory=False)


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
         
        # Asegúrate de que las columnas que usarás para fusionar tengan el mismo nombre
        # Puedes renombrar la columna si es necesario
        df_specific_year.rename(columns={'item_id': 'item_id'}, inplace=True)
        
        # Realiza la fusión utilizando merge
        df_merged = pd.merge(
            df_specific_year[['item_id', 'recommend', 'sentiment_analysis', 'fecha']],
            user_items_explode[['item_id', 'item_name']],
            on='item_id',
            how='inner')

        # Verificar si no hay datos para el año especificado
        if df_specific_year.empty:
              return {"Mensaje": "No hay datos para el año especificado"}
        
        # Filtrar por recomendaciones positivas/neutrales
        df_recomendados = df_merged[(df_merged['recommend'] == True) & (
        df_merged['sentiment_analysis'].isin([1, 2]))]
        
        # Verificar si no hay juegos recomendados para el año especificado
        if df_recomendados.empty:
                return {"Mensaje": "No hay juegos recomendados para el año especificado"}
        
        # Contar las recomendaciones por juego y obtener el top 3
        conteo_recomendaciones = df_recomendados['item_name'].value_counts().head(3)
        resultado = [{"Puesto " + str(i + 1): {"Juego": juego, "Recomendaciones": recomendaciones}}
                        for i, (juego, recomendaciones) in enumerate(conteo_recomendaciones.values())]
        
        return resultado
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
 


@app.get('/UserNotRecommend/{year}') 

async def UsersNotRecommend(year: int):
    try:
        # Filtrar por el año especificado
        df_specific_year = user_reviews_final[user_reviews_final['fecha'].dt.year == year]
    
        # Fusionar los DataFrames para obtener la información relevante
        # Suponiendo que df_specific_year y df_user_items_explode tienen un índice común en 'item_id'
        df_merged = df_specific_year[['item_id', 'recommend', 'sentiment_analysis', 'fecha']].join(
        user_items_explode.set_index('item_id')['item_name'], how='inner')

    
        # Verificar si no hay datos para el año especificado
        if df_specific_year.empty:
            return {"Mensaje": "No hay datos para el año especificado"}
    
        # Filtrar por recomendaciones negativas
        df_recomendados = df_merged[(df_merged['recommend'] == False) & (
        df_merged['sentiment_analysis'].isin([1, 2]))]
    
        # Verificar si no hay juegos recomendados para el año especificado
        if df_recomendados.empty:
            return {"Mensaje": "No hay juegos recomendados para el año especificado"}
    
        # Contar las No recomendaciones por juego y obtener el top 3
        conteo_recomendaciones = df_recomendados['item_name'].value_counts().head(3)
        resultado = [{"Puesto " + str(i + 1): {"Juego": juego, "Recomendaciones": recomendaciones}}
                     for i, (juego, recomendaciones) in enumerate(conteo_recomendaciones.items())]
    
        return resultado
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")    


@app.get('/Sentiment_analysis/{year}')

async def Sentiment_analysis(year: int):
    try:
        # Fusionar los DataFrames para obtener la información relevante
        df_merged = pd.merge(user_reviews_final[['sentiment_analysis', 'item_id']],
                             steam_games_clean[['item_id', 'release_date']],
                             left_on='item_id',
                             right_on='item_id',
                             how='inner').reset_index(drop=True)
        
        # Cambio el formato de la columna 'release_date' 
        df_merged['release_date'] = pd.to_datetime(df_merged['release_date'])
        
        # Filtrar por el año especificado en los datos de Steam
        df_year = df_merged[df_merged['release_date'].dt.year == year]
        
        if df_year.empty:
            # Devolver un mensaje si no hay datos para el año especificado
            return {"Mensaje": "No hay datos para el año especificado"}
    
        # Contar la cantidad de registros por análisis de sentimiento
        sentiment_counts = df_year['sentiment_analysis'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentimiento', 'Cantidad']
    
        # Mapear los códigos de sentimiento a etiquetas
        sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        sentiment_counts['Sentimiento'] = sentiment_counts['Sentimiento'].map(sentiment_labels)
    
        # Crear el diccionario de retorno
        result = {row['Sentimiento']: row['Cantidad'] for _, row in sentiment_counts.iterrows()}
        
        return result
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")    
  

@app.get('/recomendacion_game/{item_id: str}')

async def recomendacion_game(item_id: str):
    try:

        # Obtenemos la columna correspondiente para cada id
        columna_juego = simil_coseno[item_id]
        
        # Obtener los juegos con los mejores puntajes (menores que 1)
        games = columna_juego[columna_juego < 1.0].sort_values(ascending=False).head(5).index.tolist()
    
        return games
    except HTTPException as http_error:
    # Manejo de excepciones de HTTPException si las necesitas capturar específicamente
        raise http_error
    except Exception as e:
        # Si hay cualquier otro tipo de excepción, lanza un error HTTP 500 con detalles del error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")
