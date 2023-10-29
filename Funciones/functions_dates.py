# IMPORTACION DE LIBRERIAS
import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz
import re

def conv_posted(date_str):
    try:
        date = pd.to_datetime(date_str, format='%B %d, %Y')
    except ValueError:
        try:
            date = pd.to_datetime(date_str + ' 1900', format='%B %d %Y')
        except ValueError:
            date = pd.to_datetime('1900-01-01')
    return date.strftime('%Y-%m-%d')


fecha_defecto = '1970-01-01'

def convertReleaseFuzzy(date_str):
    
    #Si dateParser devuelve el valor fecha_defecto, simplemente devolvemos ese valor
    if date_str == fecha_defecto:
        return pd.to_datetime(fecha_defecto).date().strftime("%Y-%m-%d")
    
    #Se verifica si la fecha se encuentra en el formato deseado
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        try:
            return pd.to_datetime(date_str, format="%Y-%m-%d").date().strftime("%Y-%m-%d")
        except ValueError:
            try:
                return pd.to_datetime(date_str, format="%Y-%d-%m").date().strftime("%Y-%m-%d")
            except ValueError:
                pass
    
    #Modificaciones Especiales
    date_str = dateParser(date_str)
    
    known_formats = ['%Y-%m-%d', '%Y', '%b %Y', '%B %Y', '%d %m %Y', '%B %Y', '%B %d %Y', '%b %d %Y', '%d %b, %Y', '%Y %d %m']

    for format_str in known_formats:
        try:
            #Se intenta convertir la fecha usando el formato conocido
            return pd.to_datetime(date_str, format=format_str).date().strftime("%Y-%m-%d")
        except ValueError:
            #Si no se puede convertir con este formato, continúa probando con otros formatos
            pass

    #Si no se pudo convertir con ninguno de los formatos conocidos, busca coincidencias difusas
    for format_str in known_formats:
        for known_date_str in known_formats:
            if fuzz.ratio(date_str, known_date_str) > 80:
                return pd.to_datetime(known_date_str, format=format_str).date().strftime("%Y-%m-%d")

    #Si no se puede convertir y no se encuentra una coincidencia aproximada, devuelve fecha_defecto = 1900-01-01
    return pd.to_datetime(fecha_defecto).date().strftime("%Y-%m-%d")

def dateParser(date_str):

    #Se realiza un 'strip'
    date_str = date_str.strip()
    #Se modifica las fechas que vienen con Quarters
    date_str = re.sub(r'q1\b', '15 01', date_str.lower())
    date_str = re.sub(r'q2\b', '15 04', date_str.lower())
    date_str = re.sub(r'q3\b', '15 07', date_str.lower())
    date_str = re.sub(r'q4\b', '15 10', date_str.lower())
    #Se modifica los casos particulares
    date_str = date_str.replace('(ish),', '')
    date_str = date_str.replace('(tentative)', '')
    date_str = date_str.replace(',', '')
    date_str = date_str.replace('.', ' ')

    #Se divide la cadena en palabras
    words = date_str.lower().split(" ")
    
    seasons = ["spring", "summer", "fall", "autumn", "winter"]

    #Se aplica la limpieza de fechas informadas vagas
    if "soon" in date_str.lower() or "coming" in date_str.lower():
        date_str = fecha_defecto

    #Se aplica la limpieza de fechas informadas como "season" + YYYY
    if any(keyword in words for keyword in seasons) and len(words) == 2:
        season  = words[0]
        year    = words[1]
        if season == "spring":
            date_str = year + "-" + "05-20"
        elif season == "summer":
            date_str = year + "-" + "07-21"
        elif season == "fall" or season == "autumn":
            date_str = year + "-" + "09-22"
        elif season == "winter":
            date_str = year + "-" + "12-21" 

    #Se realiza limpieza de fechas informadas con early, end, late, h1, h2 + YYYY
    
    #Se establece una expresión regular
    year_pattern = re.compile(r'\b(early|end|late|h[12]?)?\s?(\d{4})\b', re.IGNORECASE)

    #Se realiza una busqueda de coincidencia
    match = year_pattern.search(date_str)

    if match:
        #Se extrae el año y el tipo (early, end, late, h1, h2)
        year = match.group(2)
        type_str = match.group(1).lower() if match.group(1) else ""

        #Se mapea el tipo a un mes si es necesario
        if "early" in type_str:
            month = "01"  # Enero
        elif "end" in type_str or "late" in type_str:
            month = "12"  # Diciembre
        else:
            month = "07"  # Por defecto, usa julio

        #Se combina el año y el mes en el formato deseado
        formatted_date = f"{year}-{month}-01"
        return formatted_date

    return date_str