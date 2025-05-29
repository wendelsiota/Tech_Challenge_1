from flask import Blueprint, jsonify
from flasgger import swag_from

# Criando o Blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Home'],
    'responses': {
        200: {
            'description': 'Mensagem de boas-vindas',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Bem-vindo à API do Vitibrasil!'
                    },
                    'version': {
                        'type': 'string',
                        'example': '1.0.0'
                    }
                }
            }
        }
    }
})
def home():
    """
    Endpoint raiz da API.
    

    """
    return jsonify({
        'message': 'Bem-vindo a API do Vitibrasil!',
        'version': '1.0.0'
    }), 200 