import pyodbc


def criar_tabela():
    con = pyodbc.connect('Driver={SQL Server};Server=(local);Database=Odin;Trusted_Connection=yes;')
    cursor = con.cursor()
    criar_tabela_correspondentes = """CREATE TABLE Correspondentes(
        Id INT IDENTITY PRIMARY KEY,
        TituloObra VARCHAR(600),
        Artista VARCHAR(255),
        TituloPublicao VARCHAR(500),
        AutorPublicacao VARCHAR(255),
        AnoPublicacao VARCHAR(10))"""

    try:

        cursor.execute(criar_tabela_correspondentes)
        con.commit()
        print("Tabela de correspondencias criada com sucesso!")
        cursor.close()
    except pyodbc.Error as e:
        print("Falha ao criar a tabela de correspondencias.", e)

    finally:
        if 'con' in locals():
            con.close()
