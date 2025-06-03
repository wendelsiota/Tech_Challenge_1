# Este arquivo marca o diretório como um pacote Python 

from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    
    # Configuração do JWT
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'  # Use uma chave segura em produção
    jwt = JWTManager(app)
    
    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Scraping",
            "description": "API para scraping de dados",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Digite: Bearer <seu_token>"
            }
        },
        "security": [{"Bearer": []}]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # ... resto da configuração 