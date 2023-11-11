import time

import Analise
import CriarTabelaCorrespondentes
import CriarTabelaObras
import CriarTabelaPublicacoes
import InfoScopus
import InserirDadosTabelaObras
import InserirDadosTabelaPublicacoes
import TratarArquivo


def setup():
    TratarArquivo.extrair_informacoes('Artworks.json')
    for ano in range(2017, 2024):
        InfoScopus.pesquisar_por_ano(str(ano), arquivo_existente='PublicacoesScopus.json')
    CriarTabelaObras.criar_tabela()
    CriarTabelaPublicacoes.criar_tabela()
    CriarTabelaCorrespondentes.criar_tabela()


def main():
    inicio = time.time()
    InserirDadosTabelaObras.inserir_dados_tabela()
    InserirDadosTabelaPublicacoes.inserir_dados_tabela()
    Analise.comparar()
    fim = time.time()
    print("Tempo execução:", fim - inicio)


if __name__ == '__main__':
    setup()
    main()
