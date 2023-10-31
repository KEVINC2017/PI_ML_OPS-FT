# <h1 align=center> **MLOps - Proyecto de recomendación de videojuegos - STEAM** </h1>

## **Descripción del problema**

## Introducción

El proyecto simula un rol de Data Scientist para la plataforma de videojuegos STEAM. Se pide desarrollar un sistema de consulta y recomendación de juegos a partir de los datos iniciales, este sistema estará disponible a través de una API desplegada en Render. Esto posibilitará la interacción del usuario para obtener los datos específicos sobre los videojuegos y recomendaciones personalizadas respecto a usuarios o videojuegos.

## Datos

A continuación se presenta los datasets proporcionados para el desarrollo del proyecto:

+ steam_games.json.gz:
    Este dataset contiene los datos característicos de los videojuegos, como lo son los títulos, los desarrolladores, el año de lanzamiento, los precios, entre otros.

+ user_items.json.gz:
    Este dataset contiene los videojuegos que tiene cada usuario, así como el tiempo de juego acumulado por cada uno.

+ user_reviews.json.gz:
    Este dataset contiene las reviews que los usuarios realizaron sobre los videojuegos, además contiene las recomendaciones, url's del usuario y el id de los usuarios.

## Desarrollo del Proyecto

### 1. Transformaciones y Análisis (ETL / EDA):

Se llevo a cabo la extracción, transformación y carga (ETL) de los datasets proporcionados. Los tres archivos se encontraban en formato (.gz), por lo cual se tuvieron que descomprimir. Así mismo, los datos se encontraron anidados en una columna en el caso de dos datasets('user_items', 'user_reviews'), estos fueron desanidados, para el posterior tratamiento. Para los datasets, se llevo a cabo un tratamiento por columnas: se seleccionaron aquellas columnas que serían relevantes para el posterior análisis y desarrollo del proyecto, se eliminaron los datos duplicados, se imputaron datos según el caso y se eliminaron aquellas datos nulos que no se podían imputar

De igual manera se realizó un análisis exploratorio de datos (EDA) de los datasets, con el objetivo de identificar las variables que se utilizarían para el sistema de consulta y recomendación, además se encontraron datos atípicos que posteriormente serían excluidos del proyecto, ya que fueron considerados outliers, en este caso cabe resaltar, que algunos datos atípicos no fueron considerados como outliers.

> Importante<br>
Se eliminaron usuarios considerados como outliers del proyecto, la razón de la eliminación de los mismos es por la suma de la cantidad de tiempo de sus items del inventario eran desproporcionados, estos usuarios afectarían el resultado de las consultas y recomendaciones por dicho motivo.

### 2. Feature Engineering:

En este proyecto, se aplicó un análisis de sentimiento a las reseñas de los usuarios. Para ello, se introdujo una nueva columna llamada 'sentiment_analysis'. Esta nueva columna clasificó las reseñas en función de su tono emocional, asignando calificaciones de 0 (negativo) a 2 (positivo), con un valor intermedio de 1 (neutral). El análisis se realizó utilizando la biblioteca TextBlob, una herramienta de procesamiento de lenguaje natural. La columna 'sentiment_analysis' proporciona información esencial sobre la satisfacción y percepción de los usuarios con respecto a los videojuegos. Una vez realizado el análisis de sentimiento se grabaron en archivos parquet los registros necesarios para realizar las consultas.

### 3. Modelo de Aprendizaje automático:

Se diseñó un sistema de recomendación, primero de tipo "item-item" en el que se utilizó una matriz de similitud basada en medidas de distancia de coseno entre los juegos. Esta matriz permite identificar las relaciones y similitudes entre los juegos para realizar recomendaciones basadas en esa información. Este modelo sugiere juegos similares al introducido como referencia al evaluar su similitud con otros juegos en la base de datos. En el segundo caso, el modelo "user-item" se centra en usuarios similares y recomienda juegos que les han gustado. Ambos modelos se basan en algoritmos de filtrado colaborativo y utilizan la similitud del coseno para medir la similitud entre juegos y usuarios.

En resumen, se crearon dos modelos de recomendación que generan listas de 5 juegos, ya sea ingresando el nombre de un juego o el ID de un usuario. Estos modelos se basan en la similitud de coseno. 

### 4. Desarrollo de la API

Para el desarrollo de la API se utilizó un framework FastApi, creando las siguientes funciones

+ **developer( *desarrollador)**: Presenta información sobre la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. 

+ **userdata( *User_id)**: Proporciona la cantidad de dinero gastado por el usuario, el porcentaje de recomendación basado en reseñas y cantidad de items.

+ **UserForGenre( *genero )**: Presenta al usuario con más horas jugadas para el género dado y la acumulación de horas jugadas por año.

+ **best_developer_year( *año)**: Muestra el top 3 de desarrolladores con juegos mas recomendados por usuarios para el año dado.

+ **developer_reviews_analysis( *desarrolladora)**: Muestra el desarrollador y la cantidad total de registros de reviews categorizadas por el análisis de sentimiento (Negativas y Positivas)

+ **recomendacion_juego( *id de producto)**: Proporciona una lista con 5 juegos recomendados similares al ingresado.

+ **recomendacion_usuario( *id de usuario)**: Proporciona una lista con 5 juegos recomendados para dicho usuario.

> Importante<br>
Respecto al modelo "user-item" no se pudo realizar el deploy correspondiente, esto debido a que la memoria que ofrece Render es limitada, y el conjunto de datos requeridos excede dicha capacidad. Se optó por comentar el codigo, mas si se llego a realizarla y se puede encontrar en el archivo (API.ipynb)

### 5. Deploy:

La API se ha implementado en la plataforma Render, lo que brinda a los usuarios la capacidad de interactuar con ella. Esto les permite realizar consultas y solicitar recomendaciones de videojuegos de manera conveniente y eficiente.

## Links

Video: https://youtu.be/0_7buKJccAg

Deploy: https://pi-ml-ops-ctad.onrender.com/docs