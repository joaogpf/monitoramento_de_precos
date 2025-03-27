from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prices.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=True)

with app.app_context():
    db.create_all()


@app.route('/products', methods=['GET'])
def all_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "url": p.url, "price": p.price} for p in products])



@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    url = data.get('url')

    # Faz o scraping do preço
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_str = soup.find('span',class_="a-offscreen").text.replace("R$", "").replace(",", ".")

    price = (float(price_str.replace(".", ""))/100)

    new_product = Product(name=data.get('name'), url=url, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Produto cadastrado!", "price": price})

if __name__ == '__main__':
   
    app.run(debug=True)
