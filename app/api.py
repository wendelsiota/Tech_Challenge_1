from flask import Flask
from flasgger import Swagger
from routes.scrape_route import scrape_bp, options_table

app = Flask(__name__)

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

# Registrando o Blueprint
app.register_blueprint(scrape_bp)

if __name__ == '__main__':
    app.run(debug=True)