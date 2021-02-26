from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from models import db, Client, ClientCartProducts, Product, Order, OrderToProduct, bcrypt


auth_app = Blueprint('auth', __name__,  template_folder='templates/auth', static_folder='../static')


@auth_app.route('/client/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        client = Client.query.filter_by(nickname=request.form['nickname']).first()
        if client is not None and bcrypt.checkpw(request.form['password'].encode(), client.password):
            session['nickname'] = client.nickname
            session['id'] = client.id
            session['is_authenticated'] = True
            cart_list = ClientCartProducts.query.filter_by(id=session['id']).all()
            ids = [x.product_id for x in cart_list]
            session['cart'] = [Product.query.filter_by(id=x).first() for x in ids]
            return redirect(url_for('home'))
        flash("Неправильный логин или пароль!")
    return render_template('signin.html')


@auth_app.route('/client/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        query = Client.query.filter_by(nickname=request.form['nickname']).first()
        if query is None:
            # nickname, name, password, address, phone
            client = Client(request.form['nickname'], request.form['name'], request.form['password'], request.form['address'], request.form['phone'])
            db.session.add(client)
            db.session.commit()
            return redirect(url_for('.signin'))
        flash("Пользователь с таким логином уже существует!")
    return render_template('signup.html')

@auth_app.route('/client/change_password/', methods=['GET', 'POST'])
def change_password():
    if session['is_authenticated']:
        if request.method == 'POST':
            query = Client.query.filter_by(nickname=session['nickname'])
            client = query.first()
            if client is None or not bcrypt.checkpw(request.form['old_password'].encode(), client.password):
                flash('Неправильный старый пароль!')
                return redirect(url_for('.change_password'))
            if request.form['old_password'] != request.form['password']:
                new_password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
                query.update({'password': new_password})
                flash('Ваш пароль обновлен!')
                return redirect(url_for('home'))
            flash('Вы ввели свой старый пароль!')
            return redirect(url_for('.change_password'))
        return render_template('change_password.html')
    flash('Вы должны авторизоваться!')
    return redirect(url_for('.signin'))


@auth_app.route('/client/logout/')
def logout():
    session.pop('nickname', None)
    session.pop('id', None)
    session['is_authenticated'] = False
    session.pop('cart', None)
    return redirect(url_for('home'))

@auth_app.route('/client/<int:client_id>/', methods=['GET'])
def client(client_id):
    if session['is_authenticated']:
        if session['id'] == client_id:
            orders = Order.query.filter_by(client_id=client_id).all()
            orders.reverse()
            return render_template('client.html', orders=orders)
    flash('У вас нет прав доступа.')
    return redirect(url_for('home'))

@auth_app.route('/order/add/')
def order_add():
    if session['is_authenticated'] and session['cart']!=[]:
        order = Order(session['id'])
        db.session.add(order)
        db.session.commit()
        sum = 0
        for product in session['cart']:
            o = OrderToProduct(order.id, product_id=product.id)
            sum += product.price
            db.session.add(o)
        session['cart'] = []
        ClientCartProducts.query.filter(ClientCartProducts.client_id==session['id']).delete(synchronize_session=False)
        Order.query.filter_by(id=order.id).update({'sum': sum})
        db.session.commit()
        return redirect(url_for('.client', client_id=session['id']))
    flash("Авторизуйтесь и добавьте товары в корзину для оформления заказа.")
    return redirect(url_for('home'))

@auth_app.route('/order/<int:order_id>/')
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is not None:
        if session['is_authenticated'] and session['id'] == order.client_id:
            prods = OrderToProduct.query.filter_by(order_id=order_id).all()
            ids = [x.product_id for x in prods]
            order_list = []
            for id_ in ids:
                prod = Product.query.filter_by(id=id_).first()
                order_list.append(prod)
            return render_template('order_detail.html', products=order_list, order=order)
        flash('У вас нет прав доступа.')
        return redirect(url_for('home'))
    flash('Ошибка.')
    return redirect(url_for('home'))

