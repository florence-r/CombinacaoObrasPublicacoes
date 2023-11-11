import json


def extrair_informacoes(json_data):
    try:
        with open(json_data, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {json_data}")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []

    resultados_processados = []

    try:

        for entrada in data:
            title = entrada.get("Title", "N/A")

            if len(title) > 2:
                artist_list = entrada.get("Artist", [])
                artist = artist_list[0] if artist_list else "N/A"

                date = entrada.get("Date", "N/A")

                informacoes = {
                    "title": title,
                    "artist": artist,
                    "date": date
                }

                resultados_processados.append(informacoes)

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        return []

    with open('ArtworkNovo.json', 'w', encoding='utf-8') as json_file:
        json.dump(resultados_processados, json_file, ensure_ascii=False, indent=4)

    print(f'Os resultados processados foram salvos em ArtworkNovo.json')
