# 1) Aqui lo que hemos hecho ha sido importar las librerias que vamos a utilizar. Es el paso 1

 

import os

from bs4 import BeautifulSoup

import requests

import time

import sqlite3

import matplotlib.pyplot as plt

import seaborn as sns

 

print ("todas las bibliotecas se importaron correctamente")

 

# 2) defino el url (la direccion) de la pagina de la que quiero sacar los datos:

url = "https://companies-market-cap-copy.vercel.app/index.html"

 

# 3)        METEMOS EL HTML DE LA PAGINA - ESTO ES IMPORTANTE PARA VER LA RESPUESTA DEL SERVIDOR PARA QUE SAQUEMOS LA INFORMACION QUE QUERAMOS:

import requests

 

response = requests.get(url)

if response.status_code != 200:

    print("error al acceder a la pagina")

html_content = response.text

html_content

 

# 4) metemos todo lo que haya ahi dentro osea el contenido HTML con BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")    

 

# 5) Extraigo ahora la tabla de ingresos

from bs4 import BeautifulSoup

table = soup.find("table")

table  

# 6) Extraegor las filas

 

rows = table.find_all("tr")

 

# 7) Procesamiento de  datos de la tabla de antes

data = []

for row in rows[1:]:  # Saltar la fila de encabezado

    cols = row.find_all("td")

    fecha = cols[0].text.strip()

    ingresos = cols[1].text.strip()

    data.append([fecha, ingresos])

 

# 8) monton un DataFrame con los datos extraídos

df = pd.DataFrame(data, columns=["Fecha", "Ingresos"])

 

# 9) Ordeno los datos por la columna "Fecha" de menos a mas

df = df.sort_values("Fecha")

 

df

 

# 10) ahora Limpiar y convertir los ingresos a nºs

def convertir_ingresos(valor):

    if "B" in valor:

        editar_valor = float(valor.replace("B", "").replace("$", "").replace(",", ""))

        return editar_valor

 

df["Ingresos"] = df["Ingresos"].apply(convertir_ingresos)

 

df["Ingresos"]  

 

# 11) Conectar a SQLite y guardar los datos

conn = sqlite3.connect("tesla_revenues.db")

cursor = conn.cursor()  

 

# 12) Crear tabla en SQLite

cursor.execute("""

CREATE TABLE IF NOT EXISTS ingresos (

    fecha TEXT,

    ingresos REAL

)

""")

 

# 13) Inserto datos en la base de datos

for index, row in df.iterrows():

    cursor.execute("INSERT INTO ingresos (fecha, ingresos) VALUES (?, ?)", (row["Fecha"], row["Ingresos"]))

 

conn.commit()

conn.close()

 

# 14) dibujo y hago grafico de los datos

plt.figure(figsize=(10, 6))

plt.plot(df["Fecha"], df["Ingresos"], marker='o', label="Ingresos")

plt.title("Ingresos anuales de Tesla")

plt.xlabel("Fecha")

plt.ylabel("Ingresos en billones(USD)")

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

 

# 15) Guardo y muestzro el gráfico

plt.savefig("revenue_plot.png")

plt.show()

 
