from flask import Blueprint, render_template, redirect, flash, url_for, session
from models import db, Product, ClientCartProducts, NotebookProduct, SmartphoneProduct

product_app = Blueprint('product', __name__, template_folder='templates/product', static_folder='../static')


def define_product(product_id):
    prod = Product.query.filter_by(id=product_id).first()
    if prod.category_title == 'Ноутбук':
        prod = NotebookProduct.query.filter_by(id=prod.id).first()
    elif prod.category_title == 'Смартфон':
        prod = SmartphoneProduct.query.filter_by(id=prod.id).first()
    return prod

"""
def define_product(product_id):
    return Product.query.filter_by(id=product_id).first()
"""


@product_app.route('/cart/', methods=['GET'])
def cart():
    sum = 0
    for product in session['cart']:
        sum += product.price
    return render_template('cart.html', sum=sum)

@product_app.route('/cart/add/<int:product_id>/', methods=['GET'])
def cart_add(product_id):
    product = define_product(product_id)
    if product is not None:
        session['cart'].append(product)
        if session['is_authenticated']:
            new_cart_product = ClientCartProducts(client_id=session['id'], product_id=product_id)
            db.session.add(new_cart_product)
            db.session.commit()
        flash('Товар был добавлен в вашу корзину.')
        return redirect(url_for('.product_detail', product_id=product.id))
    flash('Произошла ошибка!')
    return redirect(url_for('home'))

@product_app.route('/cart/delete/<int:product_id>/', methods=['GET'])
def cart_delete(product_id):
    product = define_product(product_id)
    ids = [x.id for x in session['cart']]
    if product.id in ids:
        session['cart'].pop(ids.index(product.id))
        if session['is_authenticated']:
            query = ClientCartProducts.query.filter_by(product_id=product.id, client_id=session['id']).first()
            db.session.delete(query)
            db.session.commit()
        flash('Товар был удалён из вашей корзины.')
        return redirect(url_for('.cart'))
    flash('Произошла ошибка!')
    return redirect(url_for('.cart'))

@product_app.route('/detail/<int:product_id>/', methods=['GET'])
def product_detail(product_id):
    product = define_product(product_id)
    return render_template('product_detail.html', product=product)

