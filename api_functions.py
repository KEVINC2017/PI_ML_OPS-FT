import pandas as pd
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

#Datos a utilizar (parquet)

df_developer = pd.read_parquet("Datasets/developer")
df_best_developer_year = pd.read_parquet("Datasets/best_developer_year")
df_developer_reviews_analysis = pd.read_parquet("Datasets/developer_reviews_analysis")
df_user_data = pd.read_parquet("Datasets/user_data")
df_user_for_genre = pd.read_parquet("Datasets/user_for_genre")

def presentation():

    try:
        html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Información General de la API</title>
            </head>
            <body>
                <h1>API Creada por Kevin Ronald Coaguila Torres</h1>
                <hr> <!-- Línea horizontal -->
                <h2>MLOPs - STEAM</h2>
                <hr> <!-- Línea horizontal -->
                <h2>Endpoints:</h2>
                <ol>
                    <li><code><strong style="color: #ff5733">/developer/</strong> (desarrolladora: str)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra la cantidad de ítems y el porcentaje de contenido Free por año, según empresa desarrolladora.</li>
                    <li><code><strong style="color: #ff5733">/userdata/</strong> (user_id: str)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra la cantidad de dinero gastado por el usuario, el porcentaje de recomendación y la cantidad de items.</li>
                    <li><code><strong style="color: #ff5733">/UserForGenre/</strong> (genre: str)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra el usuario que acumula más horas jugadas para el género dado una lista de la acumulación de horas jugadas por año de lanzamiento.</li>
                    <li><code><strong style="color: #ff5733">/best_developer_year/</strong> (year: int)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.</li>
                    <li><code><strong style="color: #ff5733">/developer_reviews_analysis/</strong> (developer: str)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra un diccionario con el nombre del desarrollador y una lista con la cantidad total de registros de reviews categorizadas por un análisis de sentimiento.</li>
                </ol>
            </body>
            </html>
        """
        return HTMLResponse(content=html_content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en presentation: {str(e)}")

def developer(desarrolladora):
    # Filtra el DataFrame para obtener las filas correspondientes a la developer
    developer_data = df_developer[df_developer['developer'] == developer]

    if developer_data.empty:
        return None

    #Se agrupa los datos por año y calcula la cantidad de items y el porcentaje de contenido Free por año
    developer_year = []
    for año, grupo in developer_data.groupby('year'):
        cantidad_items = grupo['items_count'].sum()
        contenido_free = round(grupo['free_content'].sum(),2)

        developer_year.append({"Año": año, "Cantidad de Items": cantidad_items,"Contenido Free": str(contenido_free) + " %"})
    return {'Desarrollador '+ desarrolladora : developer_year}

def userdata(user_id):
    # Filtra el df para obtener las filas segun el usuario
    user_data = df_user_data[df_user_data['user_id'] == user_id]

    if user_data.empty:
        return None

    # Se extrae el dinero gastado, el porcentaje de recomendacion y la cantidad de items del usuario
    dinero_gastado = user_data['spent'].values[0]
    porcentaje_recomendacion = user_data['percentage_recommend'].values[0]
    cantidad_items = user_data['count_items'].values[0]

    return {"Usuario": user_id, "Dinero gastado": str(dinero_gastado)+" USD"}
    #return {"Usuario": user_id, "Dinero gastado": str(dinero_gastado)+" USD", "% de recomendación": str(porcentaje_recomendacion) + " %","cantidad de items": cantidad_items}

def UserForGenre(genre):
    # Filtra el df para obtener las filas segun el genero
    user_genre_data = df_user_for_genre[df_user_for_genre['genres'] == genre]

    if user_genre_data.empty:
        return None
    
    # Se extrae el user_id y el playtime por año segun el genero
    user_id = user_genre_data['user_id'].values[0]
    playtime = list(user_genre_data['Horas_Jugadas'].values[0])

    return {'Usuario con más horas jugadas para Género '+ genre: user_id, 'Horas Jugadas': playtime}

def best_developer_year(year):
    # Filtra el df para obtener las filas segun el desarrollador
    year_data = df_best_developer_year[df_best_developer_year['Año'] == year]

    if year_data.empty:
        return None
    
    # Se extrae los nombres de los desarrolladores en el top 3 para ese año
    top_1 = year_data['Top 1'].values[0]
    top_2 = year_data['Top 2'].values[0]
    top_3 = year_data['Top 3'].values[0]

    desarrolladores_top = [{'Puesto 1': top_1}, {'Puesto 2': top_2}, {'Puesto 3': top_3}]

    return {'Año ' + str(year): desarrolladores_top}

def developer_reviews_analysis(developer):
    # Filtra el df para obtener las filas segun el desarrollador
    developer_data = df_developer_reviews_analysis[df_developer_reviews_analysis['developer'] == developer]

    if developer_data.empty:
        return None

    # Se extrae los valores positivos y negativos
    total_positive = int(developer_data['Positive'].sum())
    total_negative = int(developer_data['Negative'].sum())

    return {developer: ['Negative = '+ str(total_negative), 'Positive = '+ str(total_positive)]}

