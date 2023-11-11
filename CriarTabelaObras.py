import pyodbc
from pyodbc import Connection


def criar_tabela():
    con: Connection = pyodbc.connect('Driver={SQL Server};Server=(local);Database=Odin;Trusted_Connection=yes;')
    cursor = con.cursor()
    criar_tabela_obras = """CREATE TABLE Obras(
        Id_Obra INT IDENTITY PRIMARY KEY,
        Titulo VARCHAR(900),
        Artista VARCHAR(255))"""

    criar_indice_titulo = """
            CREATE INDEX IX_Titulo ON Obras(Titulo)
        """

    try:

        cursor.execute(criar_tabela_obras)
        con.commit()
        print("Tabela de obras criada com sucesso!")

        cursor.execute(criar_indice_titulo)
        con.commit()
        print("Índice na coluna Titulo criado com sucesso!")

        cursor.close()
    except pyodbc.Error as e:
        print("Falha ao criar tabela de obras.", e)

    finally:
        if 'con' in locals():
            con.close()
