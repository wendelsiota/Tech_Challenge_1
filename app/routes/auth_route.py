from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from utils.users import USERS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'user1'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'senha123'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Token JWT gerado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            }
        },
        400: {
            'description': 'Credenciais não fornecidas',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Credenciais não fornecidas'
                    }
                }
            }
        },
        401: {
            'description': 'Credenciais inválidas',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Credenciais inválidas'
                    }
                }
            }
        }
    }
})
def login():
    """
    Rota para autenticação e obtenção do token JWT
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Credenciais não fornecidas"}), 400

    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200 