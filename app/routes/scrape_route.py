from flask import Blueprint, request, jsonify
from services.web_scraper import scrape_table
from urllib.parse import urlencode
from flasgger import swag_from

# Criando o Blueprint
scrape_bp = Blueprint('scrape', __name__)

# Tabela Markdown com as opções e subopções
options_table = """
### Opções e Subopções Disponíveis

| Opção   | Subopção       | Descrição                       | Aceita Subopção? |
|---------|----------------|---------------------------------|------------------|
| opt_02  | -              | Produção                       | Não              |
| opt_03  | subopt_01      | Processamento - Viníferas      | Sim              |
|         | subopt_02      | Processamento - Americanas e Híbridas | Sim       |
|         | subopt_03      | Processamento - Uvas de Mesa   | Sim              |
|         | subopt_04      | Processamento - Sem Classificação | Sim           |
| opt_04  | -              | Comercialização                | Não              |
| opt_05  | subopt_01      | Importação - Vinhos de Mesa    | Sim              |
|         | subopt_02      | Importação - Espumantes        | Sim              |
|         | subopt_03      | Importação - Uvas Frescas      | Sim              |
|         | subopt_04      | Importação - Uvas Passas       | Sim              |
|         | subopt_05      | Importação - Suco de Uva       | Sim              |
| opt_06  | subopt_01      | Exportação - Vinhos de Mesa    | Sim              |
|         | subopt_02      | Exportação - Espumantes        | Sim              |
|         | subopt_03      | Exportação - Uvas Frescas      | Sim              |
|         | subopt_04      | Exportação - Suco de Uva       | Sim              |
"""

# Configuração das opções válidas
VALID_OPTIONS = {
    "opt_02": {"subopcao": None, "descricao": "Produção"},
    "opt_03": {
        "subopt_01": "Processamento - Viníferas",
        "subopt_02": "Processamento - Americanas e Híbridas",
        "subopt_03": "Processamento - Uvas de Mesa",
        "subopt_04": "Processamento - Sem Classificação"
    },
    "opt_04": {"subopcao": None, "descricao": "Comercialização"},
    "opt_05": {
        "subopt_01": "Importação - Vinhos de Mesa",
        "subopt_02": "Importação - Espumantes",
        "subopt_03": "Importação - Uvas Frescas",
        "subopt_04": "Importação - Uvas Passas",
        "subopt_05": "Importação - Suco de Uva"
    },
    "opt_06": {
        "subopt_01": "Exportação - Vinhos de Mesa",
        "subopt_02": "Exportação - Espumantes",
        "subopt_03": "Exportação - Uvas Frescas",
        "subopt_04": "Exportação - Suco de Uva"
    }
}

# Anos válidos
VALID_YEARS = range(1970, 2025)

def build_url(ano, opcao, subopcao=None):
    """
    Constrói a URL com base nos parâmetros fornecidos.

    Args:
        ano (str): Ano da consulta.
        opcao (str): Opção da consulta (ex.: opt_02).
        subopcao (str, optional): Subopção da consulta (ex.: subopt_01).

    Returns:
        str: URL construída.
    """
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    params = {"ano": ano, "opcao": opcao}
    if subopcao:
        params["subopcao"] = subopcao
    return f"{base_url}?{urlencode(params)}"

@scrape_bp.route('/scrape', methods=['GET'])
@swag_from({
    'tags': ['Scraping'],
    'parameters': [
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'Ano da consulta (ex.: 2020). Deve estar entre 1970 e 2024.',
            'minimum': 1970,
            'maximum': 2024
        },
        {
            'name': 'opcao',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Opção da consulta. Veja a tabela de opções na descrição geral da API.',
            'enum': list(VALID_OPTIONS.keys())
        },
        {
            'name': 'subopcao',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Subopção da consulta (obrigatória para algumas opções como opt_03, opt_05, opt_06). Veja a tabela de opções na descrição geral da API.',
            'enum': ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04', 'subopt_05']
        }
    ],
    'responses': {
        200: {
            'description': 'Dados extraídos com sucesso.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        },
                        'example': [["País", "Quantidade"], ["Brasil", "123456"]]
                    },
                    'url': {'type': 'string',
                            'example': 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&opcao=opt_06&subopcao=subopt_01'}
                }
            }
        },
        400: {
            'description': 'Erro nos parâmetros fornecidos.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': "Parâmetros 'ano' e 'opcao' são obrigatórios"}
                }
            }
        },
        500: {
            'description': 'Erro ao processar a URL.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'Erro ao processar a URL: HTTP Error 404'}
                }
            }
        }
    }
})
def get_table_data():
    """
    Endpoint da API que recebe ano, opcao e (opcionalmente) subopcao via query string
    e retorna os dados extraídos da tabela.

    Query Parameters:
        ano (str): Ano da consulta (ex.: 2020).
        opcao (str): Opção da consulta (ex.: opt_02).
        subopcao (str, optional): Subopção da consulta (ex.: subopt_01).

    Returns:
        JSON: Dados extraídos da tabela ou mensagem de erro.
    """
    ano = request.args.get('ano')
    opcao = request.args.get('opcao')
    subopcao = request.args.get('subopcao')

    # Validação dos parâmetros
    if not ano or not opcao:
        return jsonify({"status": "error", "message": "Parâmetros 'ano' e 'opcao' são obrigatórios"}), 400

    try:
        ano = int(ano)
        if ano not in VALID_YEARS:
            return jsonify({"status": "error",
                            "message": f"Ano inválido. Use um ano entre {min(VALID_YEARS)} e {max(VALID_YEARS)}"}), 400
    except ValueError:
        return jsonify({"status": "error", "message": "O parâmetro 'ano' deve ser um número inteiro"}), 400

    if opcao not in VALID_OPTIONS:
        return jsonify(
            {"status": "error", "message": f"Opção inválida. Opções válidas: {list(VALID_OPTIONS.keys())}"}), 400

    # Verifica se subopcao é necessária ou válida
    option_details = VALID_OPTIONS[opcao]
    if isinstance(option_details, dict) and "subopcao" in option_details and option_details["subopcao"] is None:
        if subopcao:
            return jsonify({"status": "error", "message": f"A opção '{opcao}' não aceita subopcao"}), 400
    elif isinstance(option_details, dict) and subopcao not in option_details:
        return jsonify({"status": "error",
                        "message": f"Subopção inválida para '{opcao}'. Subopções válidas: {list(option_details.keys())}"}), 400

    try:
        # Constrói a URL
        url = build_url(ano, opcao, subopcao)

        # Chama a função de scraping
        data = scrape_table(url)
        return jsonify({"status": "success", "data": data, "url": url}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao processar a URL: {str(e)}"}), 500 