import pandas as pd
from textblob import TextBlob

def sentimientoTextblob(columna,nombre_obj):
    sentimientos = []
    for texto in columna:
        if isinstance(texto, str) and texto.strip():
            analysis = TextBlob(texto)
            # Se establece el umbral para cada caso
            if analysis.sentiment.polarity < -0.2:
                # Sentimiento negativo
                sentimientos.append(0)      
            elif analysis.sentiment.polarity > 0.2:
                # Sentimiento positivo
                sentimientos.append(2)      
            else:
                # Sentimiento neutro
                sentimientos.append(1)      
        else:
            # Si no hay información en la celda, considerarlo neutro
            sentimientos.append(1)              
    return pd.Series(sentimientos, name=nombre_obj)