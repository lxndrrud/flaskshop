from flask import Flask, render_template, session, flash, redirect, url_for
from flask.globals import request
from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
from models import db, Product
from apps.product import product_app
from apps.auth import auth_app
from apps.search import search_app
from utils import max_split_on_pages, generate_pagination, paginate
import os


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.secret_key = os.environ.get('SECRET_KEY', '12123124')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# db = SQLAlchemy(app)
db.app = app
db.init_app(app)
app.config['SESSION_SQLALCHEMY'] = db
session_ = Session(app)
session_.app.session_interface.db.create_all()

app.register_blueprint(product_app)
app.register_blueprint(auth_app)
app.register_blueprint(search_app)



@app.route('/', methods=['GET'])
def home():
    if not session.get('is_authenticated', False):
        session['is_authenticated'] = False
    if not session.get('cart', False):
        session['cart'] = []
    page = request.args.get('page', 1, type=int)
    products = Product.query.all()
    max_split = max_split_on_pages(products)
    if page > max_split:
        flash('Ошибка в запросе!')
        return redirect(url_for('home'))
    products = paginate(products, page)
    pagination = generate_pagination(page, max_split)
    return render_template('home.html', products=products, page=page,  pagination=pagination)






if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
