from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from routes.scrape_route import scrape_bp, options_table
from routes.home_route import home_bp
from routes.auth_route import auth_bp

app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-aqui'  # Em produção, use uma chave segura
jwt = JWTManager(app)

# Configuração do Flasgger com a tabela na descrição
app.config['SWAGGER'] = {
    'title': 'Vitibrasil Scraper API',
    'description': (
        'API para scraping de dados do site Vitibrasil, com opções de ano, categoria e subcategoria.\n\n'
        f'{options_table}'
    ),
    'uiversion': 3,
    'version': '1.0.0'
}
swagger = Swagger(app)

# Registrando os Blueprints
app.register_blueprint(scrape_bp)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)