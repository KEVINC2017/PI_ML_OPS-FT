# Importaciones
from fastapi import FastAPI, Query
import api_functions as fa

# Se instancia la aplicacion
app = FastAPI()

#ROOT
@app.get("/")
async def home():
    '''
    Pagina de inicio que muestra la presentacion
    '''
    return fa.presentation()

# ENDPOINTS
#1 developer
@app.get(path= "/developer")
async def developer(desarrolladora: str = Query (...,
                                            description='Desarrollador de videojuegos',
                                            example='Valve')):
    '''Muestra la cantidad de ítems y el porcentaje de contenido Free por año,
    según empresa desarrolladora
    '''
    return fa.developer(desarrolladora)

#2 userdata
@app.get(path= "/userdata")
async def userdata(user_id: str = Query (...,
                                            description='Identificador único del usuario',
                                            example='76561198070565427')):
    '''Muestra la cantidad de dinero gastado por el usuario, el porcentaje
    de recomendación y la cantidad de items
    '''
    return fa.userdata(user_id)

#3 userforgenre
@app.get(path= "/UserForGenre")
async def UserForGenre(genre: str = Query (...,
                                            description='Género del videojuego',
                                            example='Action')):
    '''Muestra el usuario que acumula más horas jugadas para el género dado y
    una lista de la acumulación de horas jugadas por año de lanzamiento
    '''
    return fa.UserForGenre(genre)

#4 bestdeveloperyear
@app.get(path= "/best_developer_year")
async def best_developer_year(year: int = Query (...,
                                            description='Año para filtrar a los mejores desarrolladores',
                                            example='2015')):
    '''Muestra el top 3 de desarrolladores con juegos más recomendados por 
    usuarios para el año dado
    '''
    return fa.best_developer_year(year)

#5 developer_reviews_analysis
@app.get(path= "/developer_reviews_analysis")
async def developer_reviews_analysis(developer: str = Query (...,
                                            description='Desarrollador de videojuegos',
                                            example='Valve')):
    '''Muestra un diccionario con el nombre del desarrollador y una lista
    con la cantidad total de registros de reviews categorizadas por un 
    análisis de sentimiento
    '''
    return fa.developer_reviews_analysis(developer)

#6 recomendacion_juego
@app.get(path= "/recomendacion_juego")
async def recomendacion_juego(item_id: str = Query (...,
                                            description='Identificador único de juego',
                                            example='50')):
    '''Muestra una lista con 5 juegos recomendados similares al ingresado
    '''
    return fa.recomendacion_juego(item_id)
'''
#7 recomendacion_usuario
@app.get(path= "/recomendacion_usuario")
async def recomendacion_usuario(user_id: str = Query (...,
                                            description='Identificador único del usuario',
                                            example='-2SV-vuLB-Kg')):
        #Muestra una lista con 5 juegos recomendados para el usuario ingresado

    return fa.recomendacion_usuario(user_id)
'''