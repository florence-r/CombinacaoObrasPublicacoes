import pyodbc
from pyodbc import Connection


def criar_tabela():
    con: Connection = pyodbc.connect('Driver={SQL Server};Server=(local);Database=Odin;Trusted_Connection=yes;')
    cursor = con.cursor()
    criar_tabela_publicacoes = """CREATE TABLE Publicacoes(
        Id_Publicacao INT IDENTITY PRIMARY KEY,
        Titulo VARCHAR(255),
        Autor VARCHAR(255),
        Ano VARCHAR(10))"""

    criar_indice_titulo = """
                CREATE INDEX IX_Titulo ON Publicacoes(Titulo)
            """

    try:

        cursor.execute(criar_tabela_publicacoes)
        con.commit()
        print("Tabela de publicacoes criada com sucesso!")

        cursor.execute(criar_indice_titulo)
        con.commit()
        print("Índice na coluna Titulo criado com sucesso!")

        cursor.close()

    except pyodbc.Error as e:
        print("Falha ao criar tabela de publicacoes.", e)

    finally:
        if 'con' in locals():
            con.close()
