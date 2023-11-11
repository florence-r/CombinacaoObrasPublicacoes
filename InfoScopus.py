import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os


def pesquisar_por_ano(ano, arquivo_existente=None):
    api_key = 'x'

    initial_query_params = {
        'query': f'PUBYEAR IS {ano}',
        'apiKey': api_key,
        'httpAccept': 'application/json',
        'count': 25
    }

    response = requests.get('https://api.elsevier.com/content/search/scopus', params=initial_query_params)

    if response.status_code == 200:
        data = response.json()
        items_per_page = int(data.get('search-results', {}).get('opensearch:itemsPerPage', 25))
        columns = ['title', 'creator', 'pubyear']
        all_results_df = pd.DataFrame(columns=columns)
        all_results_df = process_results_df(all_results_df, data, ano)

        max_pages = 10
        with ThreadPoolExecutor() as executor:
            futures = []
            for page_num in range(1, max_pages):
                start_index = items_per_page * page_num

                next_page_params = {
                    'query': f'PUBYEAR IS {ano}',
                    'apiKey': api_key,
                    'httpAccept': 'application/json',
                    'count': items_per_page,
                    'start': start_index
                }

                futures.append(
                    executor.submit(make_request_and_process, all_results_df.copy(), next_page_params, ano)
                )

            for future in futures:
                all_results_df = pd.concat([all_results_df, future.result()], ignore_index=True)

        resultados_json = f'todos_os_resultados_{ano}.json'

        if arquivo_existente and os.path.exists(arquivo_existente):
            with open(arquivo_existente, 'r', encoding='utf-8') as json_file:
                existing_results = json.load(json_file)

            existing_results.extend(all_results_df.to_dict(orient='records'))

            with open(arquivo_existente, 'w', encoding='utf-8') as json_file:
                json.dump(existing_results, json_file, ensure_ascii=False, indent=4)

            print(f'Novos resultados do ano {ano} adicionados a "{arquivo_existente}"')
        else:
            with open(resultados_json, 'w', encoding='utf-8') as json_file:
                json.dump(all_results_df.to_dict(orient='records'), json_file, ensure_ascii=False, indent=4)

            print(f'Todos os resultados do ano {ano} salvos em "{resultados_json}"')
    else:
        print(f"Erro na solicitação: {response.status_code} - {response.text}")


def process_results_df(results_df, response_data, ano):

    entries = response_data.get('search-results', {}).get('entry', [])
    for entry in entries:
        cover_date = entry.get('prism:coverDate', 'N/A')
        pubyear = cover_date.split('-')[0] if '-' in cover_date else 'N/A'

        if pubyear == ano:
            result = {
                'title': entry.get('dc:title', 'N/A'),
                'creator': entry.get('dc:creator', 'N/A'),
                'pubyear': pubyear
            }
            results_df = pd.concat([results_df, pd.DataFrame([result])], ignore_index=True)

    return results_df


def make_request_and_process(results_df, params, ano):

    response = requests.get('https://api.elsevier.com/content/search/scopus', params=params)

    if response.status_code == 200:
        data = response.json()
        return process_results_df(results_df.copy(), data, ano)
    else:
        print(f"Erro na solicitação: {response.status_code} - {response.text}")



