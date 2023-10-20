from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Soni%40O2003@localhost/webapplication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Product(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100))
      description = db.Column(db.String(255))
      isDeleted = db.Column(db.Boolean, default=False)
      creationDate = db.Column(db.DateTime, default = datetime.now)
      creatorUser = db.Column(db.String(255))
      imageUrl = db.Column(db.String(255))
      categoryId = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
      categoryRel = db.relationship('Category', backref='products')


      #idcategory???

            
class Comment(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
      description = db.Column(db.String(255))
      creationDate = db.Column(db.DateTime, default = datetime.now)
      isDeleted = db.Column(db.Boolean, default=False)
      creatorUserId = db.Column(db.String(255))
    
class Category(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100))
      productRel = db.relationship('Product', backref='category', lazy=True)
      #idproduct????

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'new_column1', 'new_column2', 'creatorUser', 'imageUrl', 'categoryId', 'categoryRel')

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

product_schema = ProductSchema()
product_schema = ProductSchema(many=True)

#18:00 marshmallow

@app.route('/get', methods = ['GET'])
def get_products():
        all_products = Product.query.all()
        products_results = product_schema.dump(all_products)
        return jsonify(products_results)

@app.route('/add', methods = ['POST'])
def add_product():
      title = request.json['title']
      description = request.json['description']
      #isDeleted = request.json['isDeleted']
      creatorUser = request.json['creatorUser']
      imageUrl = request.json['imageUrl']

      new_product = Product(
        title=title,
        description=description,
        creatorUser=creatorUser,
        imageUrl=imageUrl
    )
      db.session.add(new_product)
      db.session.commit()
      return product_schema.jsonify(new_product)

@app.route('/update/<id>/', methods = ['PUT'])
def update_product(id):
      product = Product.query.get(id)

      title = request.json['title']
      description = request.json['description']
      #isDeleted = request.json['isDeleted']
      creatorUser = request.json['creatorUser']
      imageUrl = request.json['imageUrl']    
     
      product.title = title
      product.description = description
      product.creatorUser = creatorUser
      product.imageUrl = imageUrl

      db.session.commit()
      return product_schema.jsonify(product)

@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_product(id):
     product = Product.query.get(id)
     db.session.delete(product)
     db.session.commit()

     return product_schema.jsonify(product)


if __name__ == "__main__":
    # Utwórz kontekst aplikacji przed utworzeniem bazy danych
    with app.app_context():
        # Tworzenie bazy danych
        db.create_all()

    app.run(debug=True)