from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    orders = db.relationship('Order', backref=db.backref('client'))

    def __init__(self, nickname, name, password, address, phone):
        self.nickname = nickname
        self.name = name
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.address = address
        self.phone = phone

    def __repr__(self):
        return f'<User {self.id}, {self.nickname}, {self.address}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    sum = db.Column(db.Float(precision=2), nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __init__(self, client_id):
        self.client_id = client_id

    def __repr__(self) -> str:
        return f'<Order ({self.client_id})>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref=db.backref('category'))

    def __init__(self, title):
        self.title = title

    def __repr__(self) -> str:
        return f"<Category ({self.id}, {self.title})>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.Text(1000), nullable=True)
    image = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    category_title = db.Column(db.String, db.ForeignKey('category.title'))

    def __init__(self, title, category_title, price, image, description=None):
        self.title = title
        self.price = price
        self.category_title = category_title
        self.image = image
        self.description = description

    def __repr__(self) -> str:
        return f"<Product ({self.title}, {self.category_title}, {self.price})"


class NotebookProduct(Product):
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    video = db.Column(db.String(50), nullable=False)
    processor_model = db.Column(db.String(50), nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    ram_type = db.Column(db.String(10), nullable=False)

    def __init__(self, title, category_title, price, image, video, processor_model, ram, ram_type, description=None):
        super().__init__(title, category_title, price, image, description)
        self.video = video
        self.processor_model = processor_model
        self.ram = ram
        self.ram_type = ram_type

    def __repr__(self) -> str:
        return f'<Notebook ({super().title}, {self.video}, {self.processor_model})>'


class SmartphoneProduct(Product):
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    processor_model = db.Column(db.String(50), nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    inner_memory_size = db.Column(db.Integer, nullable=False)
    main_camera = db.Column(db.Integer, nullable=False)
    front_camera = db.Column(db.Integer, nullable=False)

    def __init__(self, title, category_title, price, image, processor_model, ram, inner_memory_size, main_camera, front_camera, description=None):
        super().__init__(title, category_title, price, image, description)
        self.processor_model = processor_model
        self.ram = ram
        self.inner_memory_size = inner_memory_size
        self.main_camera = main_camera
        self.front_camera = front_camera

    def __repr__(self) -> str:
        return f'<Smartphone ({super().title}, {self.ram}, {self.main_camera}, {self.front_camera})>'


class OrderToProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id

    def __repr__(self) -> str:
        return f'<OrderToProduct ({self.order_id}, {self.product_id})>'


class ClientCartProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, client_id, product_id):
        self.client_id = client_id
        self.product_id = product_id

    def __repr__(self) -> str:
        return f"<ClientCartProduct ({self.client_id}, {self.product_id})>"