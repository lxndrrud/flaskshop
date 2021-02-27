from flask import Blueprint, render_template, redirect, flash, url_for, session, request
from models import db, Product, ClientCartProducts, NotebookProduct, SmartphoneProduct, Category
from utils import paginate, max_split_on_pages, generate_pagination, check_string_arg

search_app = Blueprint('search', __name__, template_folder='templates/search', static_folder='../static')

@search_app.route('/category/', methods=['GET'])
def search_category():
    categories = Category.query.all()
    return render_template('search_category.html', categories=categories)


@search_app.route('/category/<string:category_title>/', methods=['GET', 'POST'])
def search_product(category_title):
    if not check_string_arg(category_title):
        flash('Ошибка!')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if request.args.get('page', False):
            args = session['search_filter']
            page = request.args.get('page', 1, type=int)
            if page > session['search_max_split']:
                flash('Ошибка в запросе!')
                return redirect(url_for('home'))
            result = paginate(session['search_result'], page)
            pagination = generate_pagination(page, session['search_max_split'])
            return render_template('search_product.html', products=result, category_title=category_title, filter=args, page=page, pagination=pagination)
        else:
            result = Product.query.filter_by(category_title=category_title).all()
            session['search_result'] = result
            session['search_max_split'] = max_split_on_pages(result)
            pagination = generate_pagination(1, session['search_max_split'])
            products = paginate(result, 1)
            return render_template('search_product.html', products=products, category_title=category_title, filter={}, page=1, pagination=pagination)
    else:
        args = request.form
        session['search_filter'] = args
        result = search_result(category_title, args)
        session['search_result'] = result
        session['search_max_split'] = max_split_on_pages(result)
        result = paginate(result, 1)
        pagination = generate_pagination(1, session['search_max_split'])
        return render_template('search_product.html', products=result, category_title=category_title, filter=args, page=1, pagination=pagination)


def search_result(category_title, args):
    result = []
    filter_dict = {
        'Ноутбук': {
            'func': NotebookProduct.query.filter,
            'default': NotebookProduct.query.all,
            'notebook-ram-l4': NotebookProduct.ram<4,
            'notebook-ram-4': NotebookProduct.ram==4,
            'notebook-ram-6': NotebookProduct.ram==6,
            'notebook-ram-8': NotebookProduct.ram==8,
            },
        'Смартфон': {
            'func': SmartphoneProduct.query.filter,
            'default': SmartphoneProduct.query.all,
            'smartphone-ram-l4': SmartphoneProduct.ram<4,
            'smartphone-ram-4': SmartphoneProduct.ram==4,
            'smartphone-ram-6': SmartphoneProduct.ram==6,
            'smartphone-ram-8': SmartphoneProduct.ram==8,
        }
    }
    for arg in args:
        result.extend(filter_dict[category_title]['func'](filter_dict[category_title][arg]))
    if list(args.keys()) == []:
        result = filter_dict[category_title]['default']()
    return result
