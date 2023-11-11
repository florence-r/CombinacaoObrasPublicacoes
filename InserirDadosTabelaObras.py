import pyodbc
import json


def inserir_dados_tabela():
    with open('ArtworkNovo.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    con = pyodbc.connect('Driver={SQL Server};Server=(local);Database=Odin;Trusted_Connection=yes;')
    cursor = con.cursor()
    try:
        for item in data:
            cursor.execute("INSERT INTO Obras (Titulo,Artista) VALUES (?, ?)", (item['title'], item['artist']))
            con.commit()

    except pyodbc.Error as e:
        print("Falha ao inserir os dados.", e)

    finally:
        con.close()
