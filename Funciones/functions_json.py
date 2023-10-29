# IMPORTACION DE LIBRERIAS
import pandas as pd
import gzip
import ast
import json

def descomprimirJson(path,i):
    
    datos = []
    if i == 0:
        #Se lee el archivo Json comprimido
        with gzip.open (path,"rb") as archivo:
            for linea in archivo:
                descomprimir = linea.decode('UTF-8')
                datos.append(json.loads(descomprimir))

        df = pd.DataFrame(datos)
    
    else:
        #Se lee el archivo Json comprimido
        with gzip.open (path,"rt",encoding='UTF-8') as archivo:
            datos = [ast.literal_eval(linea.strip()) for linea in archivo]
    
        df = pd.DataFrame(datos)

    return df

def desanidarJson(df, columna):

    df = df.explode(columna).reset_index(drop=True)
    df_normalizar = pd.json_normalize(df[columna])
    df_desanidado = pd.concat([df.drop(columns=[columna]),df_normalizar],axis=1)
    
    return df_desanidado