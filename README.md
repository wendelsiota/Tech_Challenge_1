# 🍇 VitiBrasil API 🍇
Este é um projeto desenvolvido para atender aos requisitos do Tech Challenge da Fase 1 do curso de MLE da FIAP, 2025.
Trata-se de uma API para consulta a dados de vitivinicultura da EMBRAPA, disponiveis no site  `http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01`.


## ⚙️Funções
- **Web Scraping**: Ferramental para raspagem de dados do site da EMBRAPA.
- **Autenticação via Token JWT**: Endpoint de raspagem protegido por toke JWT.
- **Documentação**: Documentação automática com Swagger.  



## 🪜Estrutura

```bash
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth_route.py
│   │   ├── home_route.py
│   │   └── scrape_route.py
│   ├── services
│   │   └── web_scraper.py
│   └── utils
│       └── users.py
└── README.md
└── requirements.txt
```
* **app**: Diretório principal da aplicação.
* **api.py**: Entrypoint da aplicação.
* **routes.py**: Contem as rotas organbizadas por funcionalidade.
* **services**: Ferramentas e acessórios pertinentes ao negócio (Ex.: Scraping)
* **utils**: Utilitários e acessórios (Ex.: Autenticação)
* **README.md**: Documentação do Projeto
* **requirements.txt**: Dependencias da aplicação

## 🚂Como Rodar

### 1. Clone o Repositório

```bash
git clone https://github.com/wendelsiota/Tech_Challenge_1
cd Tech_Challenge_1
```

### 2. Crie o Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as Dependencias

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação

```bash
python api.py
```
O aplicativo estará disponível em `http://localhost:5000`.

## 🛠️ Operação 

O sistema irá disponibilizar 3 endpoints:

`http://127.0.0.1:5000/` : Endpoint raiz da API (Home): Retorna uma mensagem de boas vindas que pode ser customizada com informações relevantes
`http://127.0.0.1:5000/login`: Endpoint para obtenção do token JWT, que permitirá o acesso aos endpoints que exigem autenticação
`http://127.0.0.1:5000/scrape`: Endpoint autenticado da API que recebe ano, opcao e (opcionalmente) subopcao via query string e retorna os dados extraídos do site da EMBRAPA.

### Passo 1: Obtenha o token: 
A API conta inicialmente com dois usuarios cadastrados no arquivo `utils\users.py` a título de exemplo (não é recomendado usar esta abordagem em produção).

Acesse o Endpoint de login (`http://127.0.0.1:5000/login`) passando os dados do usuario no corpo da requisição. A resposta deve ser um `access_token` que servirá para autenticar o acesso a endpoints protegidos

```bash
{
  "password": "senha123",
  "username": "user1"
}
```
É possivel obter o token através do CURL:

```bash
curl -X POST "http://127.0.0.1:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"password\": \"senha123\", \"username\": \"user1\"}"
```

### Passo 2: Raspando dados do Site da EMBRAPA:

O site da EMBRAPA divide as informações por CATEGORIA, SUBCATEGORIA e ANO.
Estas tres informações devem ser passadas ao endpoint de scrape para que a consulta seja retornada em formato `json`.
A tabela a seguir  serve como guia para construção das requisições:

 Opções e Subopções Disponíveis

| Opção   | Subopção       | Descrição                              | Aceita Subopção? |
|---------|----------------|----------------------------------------|------------------|
| opt_02  | -              | Produção                               | Não              |
| opt_03  | subopt_01      | Processamento - Viníferas              | Sim              |
|         | subopt_02      | Processamento - Americanas e Híbridas  | Sim              |
|         | subopt_03      | Processamento - Uvas de Mesa           | Sim              |
|         | subopt_04      | Processamento - Sem Classificação      | Sim              |
| opt_04  | -              | Comercialização                        | Não              |
| opt_05  | subopt_01      | Importação - Vinhos de Mesa            | Sim              |
|         | subopt_02      | Importação - Espumantes                | Sim              |
|         | subopt_03      | Importação - Uvas Frescas              | Sim              |
|         | subopt_04      | Importação - Uvas Passas               | Sim              |
|         | subopt_05      | Importação - Suco de Uva               | Sim              |
| opt_06  | subopt_01      | Exportação - Vinhos de Mesa            | Sim              |
|         | subopt_02      | Exportação - Espumantes                | Sim              |
|         | subopt_03      | Exportação - Uvas Frescas              | Sim              |
|         | subopt_04      | Exportação - Suco de Uva               | Sim              |
"""




## 🧻Documentação
A documentação da API é gerada automaticamente com Swagger e estará disponivel em `http://localhost:5000/apidocs/`.