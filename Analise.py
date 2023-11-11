import pyodbc


def comparar():
    con = pyodbc.connect('Driver={SQL Server};Server=(local);Database=Odin;Trusted_Connection=yes;')
    cursor = con.cursor()
    consulta = """INSERT INTO Correspondentes (TituloObra, Artista, TituloPublicao, AutorPublicacao, AnoPublicacao)
                  SELECT
                  O.TITULO AS TituloObra,
                  O.ARTISTA AS Artista,
                  TP.TITULO AS TituloPublicao,
                  TP.AUTOR AS AutorPublicacao,
                  TP.ANO AS AnoPublicacao
                  FROM Obras AS O
                  INNER JOIN PUBLICACOES AS TP ON TP.TITULO LIKE '% ' + O.TITULO + ' %'"""

    try:
        cursor.execute(consulta)
        con.commit()

    except pyodbc.Error as e:
        print("Falha ao inserir os dados  correspondentes.", e)

    finally:
        con.close()
