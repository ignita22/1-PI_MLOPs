<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL MACHINE LEARNING OPERATIONS** </h1>
<h2 align='center'>Darío Ignacio Aveiro</h2>


# Introducción:

En este proyecto, se basará en un estudio referido a un dataset de la plataforma STEAM, en el cuál deberemos analizar los datos, transformarlos y estandarizarlos para poder trabajar mejor en el modelado de los mismos, poder comprender la relación entre variables y así poder cumplir con los objetivos propuestos.

# Desarrollo

Se realizará un ETL (Extracción, transformación y carga) de los datos de cada archivo, con los cuales trabajaremos: user_reviews, user_items y steam_games.
Luego haremos un EDA (Análisis exploratorio de datos) también en cada uno para ver la relación entre variables, valores atípicos para poder ayudar al sistema de predicción que desarrollaremos posteriormente.

Feature Engineering: 

En el dataset user_reviews, crearemos una columna llamada 'sentiment_analysis' aplicando análisis de sentimiento con NLP con la siguiente escala: debe tomar el valor '0' si es malo, '1' si es neutral y '2' si es positivo. Esta nueva columna debe reemplazar la de user_reviews.review para facilitar el trabajo de los modelos de machine learning y el análisis de datos. De no ser posible este análisis por estar ausente la reseña escrita, debe tomar el valor de 1.

# Funciones a desarrollar desde la API para correr con Render:

+ def **PlayTimeGenre( *`genero` : str* )**:
    Debe devolver `año` con mas horas jugadas para dicho género.

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

+ def **UsersRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)

+ def **UsersNotRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)

+ def **sentiment_analysis( *`año` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
  
# Modelo de aprendizaje automático:

Se propone entrenar nuestro modelo de machine learning para armar un sistema de recomendación.
Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación. En este caso, yo utilicé el modelo de recomendación item-item.


Si es un sistema de recomendación item-item:
+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

Si es un sistema de recomendación user-item:
+ def **recomendacion_usuario( *`id de usuario`* )**:
    Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.



<div style="display: flex; align-items: center;">
  <a href="https://www.linkedin.com/in/darío-aveiro/" style="margin-right: 10px;">
    <img src="./images/in_linked_linkedin_media_social_icon_124259.png" alt="LinkedIn" width="40" height="40">
  </a>
