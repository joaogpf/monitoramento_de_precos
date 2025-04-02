from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prices.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=True)

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    old_price = db.Column(db.Float)
    new_price = db.Column(db.Float)
    price_variation = db.Column(db.Float)  # Variação do preço
    date = db.Column(db.DateTime, default=datetime.now())

with app.app_context():
    db.create_all()

#rota para selecionar todos os produtos
@app.route('/products', methods=['GET'])
def all_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "url": p.url, "price": p.price} for p in products])

#rota para editar produto
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    
    data = request.json
    product.name = data.get("name", product.name)
    product.url = data.get("url", product.url)
    product.price = data.get("price", product.price)

    db.session.commit()

    return jsonify({"message": "Produto Alterado com Sucesso!"})

#função que vai atualizar o preço dos produtos em um determinado espaço de tempo
def update_all_products():
    with app.app_context():
        products = Product.query.all()
        if products:
            for product in products:
                response = requests.get(product.url)
                soup = BeautifulSoup(response.text, 'html.parser')
                price_str = soup.find('span',class_="a-offscreen").text.replace("R$", "").replace(",", ".")
                product.price = (float(price_str.replace(".", ""))/100)
           
                db.session.commit()
        else:
            print("error ao obter produtos")

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_all_products, trigger='interval', seconds=20)
scheduler.start()


#rota para adicionar produto
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    url = data.get('url')

    # Faz o scraping do preço
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('span', id="productTitle").text
    price_str = soup.find('span',class_="a-offscreen").text.replace("R$", "").replace(",", ".")

    price = (float(price_str.replace(".", ""))/100)

    new_product = Product(name=name, url=url, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Produto cadastrado!", "price": price})

if __name__ == '__main__':
   
    app.run(debug=True)
